let gallerycount = document.getElementById('count');
gallerycount.innerText = gallerycount.innerText.replace("0",document.getElementsByClassName('item').length);