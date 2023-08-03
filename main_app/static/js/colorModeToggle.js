/**
 * Used by dark/light mode button in the navbar.html
 * Handles toggling color mode, sets
 */
window.addEventListener("load", () => {
    const colorModeBtn = document.getElementById("color-mode-btn");
    colorModeBtn.addEventListener("click", () => {
        setColorMode(true);
        setColorModeText(colorModeBtn, getColorMode());
    });

    setColorMode(false);
    setColorModeText(colorModeBtn, getColorMode());
});


function getColorMode() {
    return document.querySelector("html").getAttribute("data-bs-theme");
}

/**
 * Set the color mode and save it in local storage / database
 * @param flip {boolean} whether to flip "light"/"dark"
 * @returns {Promise<boolean>}
 */
async function setColorMode(flip = false) {
    const html = document.querySelector("html");

    let mode = html.getAttribute("data-bs-theme");
    if (!mode)
        mode = getCookies().get("color_mode");
    if (!mode)
        mode = "light";

    if (flip)
        mode = (mode === "light") ? "dark" : "light";

    // apply the mode directly via bootstrap
    html.setAttribute("data-bs-theme", mode);

    // save mode
    // set color_mode cookie, expires in one year
    const yearFromNow = new Date;
    yearFromNow.setFullYear(yearFromNow.getFullYear() + 1);
    document.cookie = "color_mode=" + mode + "; expires=" + yearFromNow + "; path=/;";

    // if not a guest, save the user's profile settings
    if (html.dataset["guest"] === "false") {
        // make the url ( e.g. https://brokemans-gamestation.com/api/color-mode/dark )
        const url = window.location.protocol + "//" + window.location.host +
            "/api/color-mode/" + mode;
        try {
            await fetch(url);
        } catch(e) {
            console.error(e);
        }
    }

    return true;
}

function setColorModeText(btn, mode) {
    btn.innerHTML = (mode === "light") ? "<i class='bi bi-sun-fill'></i>" : "<i class='bi bi-moon-stars-fill'>";

    // set iframe background if there is one
    document.getElementsByName("iframe").forEach(iframe => {
        iframe.style.background = (mode === "light") ? "#FEFEFE" : "#222";
    });
}
