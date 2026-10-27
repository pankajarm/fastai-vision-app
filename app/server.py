from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import uvicorn, aiohttp, asyncio, hashlib, torch
from io import BytesIO
from fastai.vision import *
from fastai import *

model_file_url = 'https://www.dropbox.com/s/6bgq8t6yextloqp/export.pkl?raw=1'
model_file_name = 'export.pkl'
MODEL_SHA256 = '6c3e3a33a3f4eb20c9680795acd3a75b3e1714a70320abed3abd3184fbec2bc9'
classes = ['black', 'grizzly', 'teddys']
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))

async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f: f.write(data)

def _sha256(file_path):
    h = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


async def setup_learner():
    model_path = path/'models'/f'{model_file_name}'
    await download_file(model_file_url, model_path)
    if _sha256(model_path) != MODEL_SHA256:
        raise RuntimeError('Model checksum mismatch - refusing to load')
    # fastai 1.x pickles must load with weights_only=False; torch >= 2.6
    # defaults to True. The checksum above pins the trusted artifact.
    _orig_load = torch.load
    torch.load = lambda *a, **k: _orig_load(*a, **{**k, 'weights_only': False})
    try:
        learn = load_learner(path/'models', model_file_name)
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise
    finally:
        torch.load = _orig_load

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()

PREDICTION_FILE_SRC = path/'static'/'predictions.txt'

async def upload(request):
    form = await request.form()
    img_bytes = await (form["file"].read())
    return predict_from_bytes(img_bytes)

def predict_from_bytes(bytes):
    img = open_image(BytesIO(bytes))
    _,_,losses = learn.predict(img)
    predictions = sorted(zip(classes, map(float, losses)), key=lambda p: p[1], reverse=True)
    result_html1 = path/'static'/'result1.html'
    result_html2 = path/'static'/'result2.html'
    
    result_html = str(result_html1.open().read() +str(predictions[0:3]) + result_html2.open().read())
    return HTMLResponse(result_html)

def form(request):
    index_html = path/'static'/'index.html'
    return HTMLResponse(index_html.open().read())

app.router.routes.append(Route("/upload", upload, methods=["POST"]))
app.router.routes.append(Route("/", form))

if __name__ == "__main__":
    if "serve" in sys.argv: uvicorn.run(app, host="0.0.0.0", port=8080)
