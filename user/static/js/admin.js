let all = document.getElementsByClassName('report-item');
let msg = document.getElementById('ad-desp');
let navbar = document.getElementsByClassName('home');

navbar[0].style.opacity=0;
msg.innerText = "Currently,There are "+all.length+" reports to be solved.";
