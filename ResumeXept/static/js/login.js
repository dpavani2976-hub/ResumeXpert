const theme=document.querySelector(".theme-switch");

const icon=document.getElementById("themeIcon");

theme.onclick=()=>{

document.body.classList.toggle("dark");

if(document.body.classList.contains("dark")){

icon.classList.remove("fa-moon");

icon.classList.add("fa-sun");

localStorage.setItem("theme","dark");

}else{

icon.classList.remove("fa-sun");

icon.classList.add("fa-moon");

localStorage.setItem("theme","light");

}

};

window.onload=()=>{

if(localStorage.getItem("theme")=="dark"){

document.body.classList.add("dark");

icon.classList.remove("fa-moon");

icon.classList.add("fa-sun");

}

};

const eye=document.getElementById("eye");

const pass=document.getElementById("password");

eye.onclick=()=>{

if(pass.type==="password"){

pass.type="text";

eye.classList.remove("fa-eye");

eye.classList.add("fa-eye-slash");

}else{

pass.type="password";

eye.classList.remove("fa-eye-slash");

eye.classList.add("fa-eye");

}

};