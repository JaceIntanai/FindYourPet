/* dog side // cat side effect */
var card = document.getElementsByClassName("petcard");
var l = document.getElementsByClassName("myleft");
var r = document.getElementsByClassName("myright");
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
/* ------------------- */
var slideIndex = 1;
var lastIndex =1;
function plusDivs(n,num) {
  lastIndex = slideIndex;
  showDivs(slideIndex += n,num);
}
async function showDivs(n,num) {
  let i;
  let x = card;
  if (slideIndex > x.length) {slideIndex = 1}
  if (slideIndex < 1) {slideIndex = x.length}
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
    x[i].classList.remove("LeftSlideIn");
    x[i].classList.remove("RightSlideIn");
    x[i].classList.remove("LeftSlideOut");
    x[i].classList.remove("RightSlideOut");
  }
  if(num==1){
    x[slideIndex%(x.length)].style.display = "block";
    x[slideIndex%(x.length)].classList.add("LeftSlideOut")

    await sleep(500);
    x[slideIndex%(x.length)].style.display = "none";

    x[slideIndex-1].style.display = "block";
    x[slideIndex-1].classList.add("LeftSlideIn");
  }
  else if(num==2){
    if(slideIndex==1){
      x[x.length-1].style.display = "block";
      x[x.length-1].classList.add("RightSlideOut")

      await sleep(500);
      x[x.length-1].style.display = "none";

      x[0].style.display = "block";
      x[0].classList.add("RightSlideIn");
    }
    else{
      x[(slideIndex-2)%(x.length)].style.display = "block";
      x[(slideIndex-2)%(x.length)].classList.add("RightSlideOut")

      await sleep(500);
      x[(slideIndex-2)%(x.length)].style.display = "none";

      x[slideIndex-1].style.display = "block";
      x[slideIndex-1].classList.add("RightSlideIn");
    }
  }
}
var pathname = window.location.pathname;
let c = document.getElementById("count");
if(pathname=="/pet"){c.innerText += "Currently, We have "+card.length+" pets in our community."}
if(pathname=="/search"){c.innerText += "We found "+card.length+" pets from your search definition."}