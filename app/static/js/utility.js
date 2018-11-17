var FILE_CHANGE_FLAG = false;

var el = x => document.getElementById(x);

var submit_btn = document.getElementById('submit_btn').addEventListener('mouseover', submit_btn_mouseover);

function submit_btn_mouseover(e) {
    if (!FILE_CHANGE_FLAG) {
        alert('Please choose image file before Submission!');
    }
}


var upload_img = document.getElementById('inp_file').addEventListener('change', fileChange, false);

function fileChange(e) {
    FILE_CHANGE_FLAG = true;
    document.getElementById('inp_img').value = '';

    var file = e.target.files[0];

    if (file.type == "image/jpeg" || file.type == "image/png") {

        var reader = new FileReader();  
        reader.onload = function(readerEvent) {

            var image = new Image();
            image.onload = function(imageEvent) {	
                var max_size = 420;
                var w = image.width;
                var h = image.height;
                // console.log("width:",w, "height:", h);
                if (w > h) {
                    if (w > max_size) { h*=max_size/w; w=max_size; }
                } else     {  if (h > max_size) { w*=max_size/h; h=max_size; } }
                // console.log("Updated width:",w, "Updated height:", h);

                var canvas = document.createElement('canvas');
                // FORCEFUL to portrait mode only images
                if (w > h) {
                    // canvas.width = h;
                    // canvas.height = w;
                    canvas.width = w;
                    canvas.height = h;
                    var ctx = canvas.getContext('2d');
                    // move the rotation point to the center of the rect
                    // ctx.translate( h / 2, w / 2);
                    ctx.translate( w / 2, h / 2);
                    ctx.rotate(90 * Math.PI / 180);
                    // ctx.drawImage(image, -h / 2, -w / 2, h, w);
                    ctx.drawImage(image, -w / 2, -h / 2, w, h);
                }
                else {
                    canvas.width = w;
                    canvas.height = h;
                    canvas.getContext('2d').drawImage(image, 0, 0, w, h);
                }
                if (file.type == "image/jpeg") {
                var dataURL = canvas.toDataURL("image/jpeg");

                } else {
                var dataURL = canvas.toDataURL("image/png");
                }
                el('image-picked').src = dataURL;
                el('image-picked').className = '';
                // before sending to server, split dataURL to send only data bytes
                data_bytes = dataURL.split(',');
                document.getElementById('inp_img').value = data_bytes[1];
                // console.log("data_bytes:", data_bytes);
            }
            image.src = readerEvent.target.result;
        }
        reader.readAsDataURL(file);
    } else {
        document.getElementById('inp_file').value = '';	
        alert('Please select image only in JPG or PNG format!');	
    }
}