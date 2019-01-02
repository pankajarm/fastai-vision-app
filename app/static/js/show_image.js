var dataImage = localStorage.getItem('imgData');
saved_image = document.getElementById('saved_image');
saved_image.src = "data:image/jpeg;base64," + dataImage;