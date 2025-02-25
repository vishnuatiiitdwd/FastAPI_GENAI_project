function showSignup() {
    document.getElementById("signupForm").style.display = "block";
    document.getElementById("loginForm").style.display = "none";
    document.getElementById("fileUploader").style.display = "none";
    document.getElementById("welcome-page").style.display = "none";
    document.querySelector(".transistion").style.display = "none";
}

function showLogin() {
    document.getElementById("signupForm").style.display = "none";
    document.getElementById("loginForm").style.display = "block";
    document.getElementById("fileUploader").style.display = "none";
    document.getElementById("welcome-page").style.display = "none";
    document.querySelector(".transistion").style.display = "none";
}

function showUploader() {
    document.getElementById("signupForm").style.display = "none";
    document.getElementById("loginForm").style.display = "none";
    document.getElementById("fileUploader").style.display = "block";
    document.getElementById("welcome-page").style.display = "none";
    document.querySelector(".transistion").style.display = "none";
}
function showhome(){
    document.getElementById("signupForm").style.display = "none";
    document.getElementById("loginForm").style.display = "none";
    document.getElementById("fileUploader").style.display = "none";
    document.getElementById("welcome-page").style.display = "block";
    document.querySelector(".transistion").style.display = "block";
}
