var welcome_modal = document.getElementById("Welcome_Modal");

var start_ = document.getElementsByClassName("startbtn");

var closemodal = document.getElementsByClassName("close")[0];

start_.onclick = function() {
    welcome_modal.style.display = "block";
  }

closemodal.onclick = function() {
    welcome_modal.style.display = "none";
}
window.onclick = function(event) {
    if (event.target == modal) {
      welcome_modal.style.display = "none";
    }
}
