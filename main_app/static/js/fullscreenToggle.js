/**
 * File: fullscreenToggle.js
 * Frontend script
 * Used for fullscreen button interactivity in the games/detail.html template
 * Handles toggling fullscreen button behavior class & icon
 *
 * Requirements:
 * - Bootstrap 5 and Bootstrap icons loaded in template
 * - one <iframe> element placed in the template file
 * - button (of any element type) with id: "fullscreen-btn"
 * - necessary styling for css class "fullscreen" added elsewhere
 *
 * Comment:
 * This script would be better encapsulated in a component like React
 */

// encapsulate in module for clean global namespace
(function() {

    // driver code
    window.addEventListener("load", evt => {
        // get elements
        const iframe = document.querySelector("iframe");
        const fullscreenEl = document.getElementById("fullscreen-btn");

        // add listener
        fullscreenEl.addEventListener("click", () =>
            toggleFullscreen(iframe, fullscreenEl));
    });

    /**
     * Helper to toggle "fullscreen" class and apply icons to button
     * @param iframe {HTMLElement}       iframe game screen element
     * @param fullscreenEl {HTMLElement} fullscreen toggle button element
     */
    function toggleFullscreen(iframe, fullscreenEl) {
        iframe.classList.toggle("fullscreen");
        fullscreenEl.classList.toggle("fullscreen");

        if (fullscreenEl.classList.contains("fullscreen")) {
            fullscreenEl.innerHTML = "<i class='bi bi-fullscreen-exit'></i>";
        } else {
            fullscreenEl.innerHTML = "<i class='bi bi-fullscreen'></i>"
        }
    }

})();

