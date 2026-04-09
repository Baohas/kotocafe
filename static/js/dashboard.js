function confirm(){
    container = document.getElementById("container");
    container.classList.add("blur");
    conf = document.getElementById("confirm");
    conf.classList.remove("hidden");
};
function confirm_close(){
    container = document.getElementById("container");
    conf = document.getElementById("confirm");
    container.classList.remove("blur");
    conf.classList.add("hidden");
}