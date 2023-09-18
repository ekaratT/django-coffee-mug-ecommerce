const slider = document.querySelector(".product-scroller");
const arrowBtns = document.querySelectorAll(".btn-card");
const firstCardWidth = slider.querySelector(".product-card").offsetWidth;
let isDrag = false;
let startX;
let startScrollLeft;

arrowBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        slider.scrollLeft += btn.id === "btn-left" ? -firstCardWidth : firstCardWidth;
    })
})

const dragStart = (e) => {
    isDrag = true;
    // slider.classList.add("dragging")
    slider.forEach(slid => {
        slid.classList.add("dragging");
    })
    // Records the initial cursor and scroll position of the slider
    startX = e.pageX;
    startScrollLeft = slider.scrollLeft;
}
const dragging = (e) => {
    if (!isDrag) return;
    // Update the scroll position of the slider based on the cursure movement
    slider.scrollLeft = startScrollLeft - (e.pageX - startX);
}

const dragStop = () => {
    isDrag = false;
    slider.classList.remove("dragging")
}
document.addEventListener("click", function (e) {
    if (e.target.className === "menu-list" || e.target.className === "menu-list list-active" || e.target.className === "menu-list logout" || e.target.className === "menu-text") {
        hideMenuBtn()
    }
})


function openMenu(x) {
    // x.classList.toggle("change");
    var sideBar = document.getElementById("sidebar");

    if (sideBar.className === "sidebar") {
        sideBar.className += " responsive";
    } else {
        sideBar.className = "sidebar";
    }
}


function hideMenuBtn() {
    var menu = document.getElementById("sidebar");
    menu.classList.remove("responsive")

}


slider.addEventListener("mousedown", dragStart);
slider.addEventListener("mousemove", dragging);
document.addEventListener("mouseup", dragStop);

