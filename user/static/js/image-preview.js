/* recall all variable to be used in this JS effect file */
var short = document.getElementById('brief-short').style;
var long = document.getElementById('brief-long').style;
var brief = document.getElementById('brief');
var icon = document.getElementById('regis-icon').style;
var regis = document.getElementById('upload-preview');
var wrap = document.getElementById('upload-wrapper').style;

/* Register Icon Effect */

var registerIconIn = function(event){
  console.log('icon');
    wrap.height="120px";
    wrap.transition="1s";
    icon.fontSize="2.0em";
    icon.top="-120px";
    icon.left="70px";
    icon.transition="1s";
}
var registerIconOut = function(event){
  console.log('back icon');
    wrap.height="60px";
    wrap.transition="1s";
    icon.fontSize="1.4em";
    icon.position="relative";
    icon.top="-70px";
    icon.left="35px";
    icon.transition="1s";
}
regis.addEventListener('mouseover',registerIconIn);
regis.addEventListener('mouseleave',registerIconOut);

/* Main Image-Preview Effect */

var previewImage = function(event){
  let reader = new FileReader();
  let click = document.getElementById('upload-icon').style;
  let output = document.getElementById('upload-preview').style;
  reader.onload = function(){
    click.display='none';
    output.backgroundImage='url('+reader.result+')';
    output.display='grid';
  }
  reader.readAsDataURL(event.target.files[0]);
};

var previewImageFixed = function(event){
  let reader = new FileReader();
  let output = document.getElementById('upload-preview').style;
  reader.onload = function(){
    output.backgroundImage='url('+reader.result+')';
  }
  reader.readAsDataURL(event.target.files[0]);
};

/* Register Sliding Info Effect */

var slideInInfo = function(event){

    //short.display="none";
    short.opacity="0";
    short.transition="0.5s";
    //long.display="grid";
    long.width="100%";
    long.opacity="100%";
    long.transition="1.5s";
}
var slideOutInfo = function(event){

    //short.display="grid";
    short.opacity="100%";
    short.transition="1.5s";
    //long.display="none";
    long.width="0%";
    long.opacity="0";
    long.transition="0.3s";
}
brief.addEventListener('mouseover',slideInInfo);
brief.addEventListener('mouseleave',slideOutInfo);
