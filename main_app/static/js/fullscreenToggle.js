window.addEventListener("load", evt => {
    const iframe = document.querySelector("iframe");
    const fullscreenEl = document.getElementById("fullscreen-btn");
    function toggleFullscreen() {
        iframe.classList.toggle("fullscreen");
        fullscreenEl.classList.toggle("fullscreen");

        if (fullscreenEl.classList.contains("fullscreen")) {
            fullscreenEl.innerHTML = "<i class='bi bi-fullscreen-exit'></i>";
        } else {
            fullscreenEl.innerHTML = "<i class='bi bi-fullscreen'></i>"
        }
    }


    fullscreenEl.addEventListener("click", evt => {
        toggleFullscreen();
    });
});