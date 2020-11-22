let all = document.getElementsByClassName('report-status');
for (i = 0; i < all.length; i++) {
    if(all[i].innerText=="REVIEWED"){
        all[i].innerHTML="&#128516 This issue had been reviewed.";
        all[i].style.color="rgb(34, 139, 34)";
    }
    else if(all[i].innerText=="NOT REVIEWED"){
        all[i].innerHTML="&#129300 This issue is still opened.";
        all[i].style.color="rgb(178, 34, 34)";
    }
}