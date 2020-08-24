# fastai-vision-app

PLEASE READ: This repo is now archived and replaced by latest FASTAI Version 2 repo =>  https://github.com/psmathur/fastai2-vision-app


Production ready starter pack for creating fast responsive Web App for Fast.AI Image models using Starlette.io framework with Uvicorn ASGI server.

Everything packaged in docker with requirement.txt, so you can push it to any docker hosted cloud service. Enjoy :)

You can test your changes locally by installing Docker and using the following command:

docker build -t fastai-v1 . && docker run --rm -it -p 8080:8080 fastai-v1

Few dockers hosted services where this starter pack will work =>

* https://render.com
* https://zeit.co/now
* https://azure.microsoft.com/en-us/services/app-service/containers/
* https://getcarina.com/
* https://sloppy.io/en/
* https://giantswarm.io
* https://aws.amazon.com/ecs/
* https://cloud.google.com/cloud-build/docs/
* https://www.digitalocean.com/products/one-click-apps/docker/
