// Theme Toggle

const theme=document.querySelector(".theme-switch");

const icon=document.getElementById("themeIcon");

theme.onclick=()=>{

document.body.classList.toggle("dark");

if(document.body.classList.contains("dark")){

icon.classList.replace("fa-moon","fa-sun");

localStorage.setItem("theme","dark");

}else{

icon.classList.replace("fa-sun","fa-moon");

localStorage.setItem("theme","light");

}

};

window.onload=()=>{

if(localStorage.getItem("theme")=="dark"){

document.body.classList.add("dark");

icon.classList.replace("fa-moon","fa-sun");

}

};

// Password Toggle

const pass=document.getElementById("password");

const confirm=document.getElementById("confirmPassword");

const eye1=document.getElementById("togglePassword");

const eye2=document.getElementById("toggleConfirm");

eye1.onclick=()=>{

pass.type=pass.type==="password"?"text":"password";

eye1.classList.toggle("fa-eye");

eye1.classList.toggle("fa-eye-slash");

};

eye2.onclick=()=>{

confirm.type=confirm.type==="password"?"text":"password";

eye2.classList.toggle("fa-eye");

eye2.classList.toggle("fa-eye-slash");

};

// Password Strength

const bar=document.getElementById("strengthBar");

const text=document.getElementById("strengthText");

pass.addEventListener("keyup",()=>{

let p=pass.value;

let strength=0;

if(p.length>=8) strength++;

if(/[A-Z]/.test(p)) strength++;

if(/[0-9]/.test(p)) strength++;

if(/[!@#$%^&*]/.test(p)) strength++;

if(strength==1){

bar.style.width="25%";

bar.style.background="red";

text.innerHTML="Weak Password";

}
else if(strength==2){

bar.style.width="50%";

bar.style.background="orange";

text.innerHTML="Medium Password";

}
else if(strength==3){

bar.style.width="75%";

bar.style.background="#2563EB";

text.innerHTML="Good Password";

}
else if(strength==4){

bar.style.width="100%";

bar.style.background="green";

text.innerHTML="Strong Password";

}
else{

bar.style.width="0%";

text.innerHTML="Password Strength";

}

});