// Write your JavaScript code.
let lastScrollTop = 0;
const body = document.body;

window.addEventListener("scroll", () => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    body.classList.add("is-scrolled")
    if (scrollTop > lastScrollTop) {
        // Scrolling down
        body.classList.remove("is-scrolling-up");
        body.classList.add("is-scrolling-down");
    } else {
        // Scrolling up
        body.classList.remove("is-scrolling-down");
        body.classList.add("is-scrolling-up");
    }

    if (scrollTop == 0) {
        body.classList.remove("is-scrolling-up")
        body.classList.remove("is-scrolled")
    }

    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
});
