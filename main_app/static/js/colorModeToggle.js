/**
 * Used by dark/light mode button in the navbar.html
 * Handles toggling color mode, sets
 */
window.addEventListener("load", async evt => {

    async function setColorMode(flip = false) {
        const html = document.querySelector("html");
        const _cookies = getCookies();
        let mode = html.getAttribute("data-bs-theme");
        if (!mode)
            mode = _cookies.get("color_mode");
        if (!mode) {
            mode = "light";
        }

        if (flip)
            mode = (mode === "light") ? "dark" : "light";


        document.cookie = "color_mode=" + mode + "; expires=" + Date.now() + "; path=/;";

        html.setAttribute("data-bs-theme", mode);

        const url = window.location.protocol + "//" + window.location.host +
            "/api/color-mode/" + mode;

        if (html.dataset["guest"] === "false") {
            try {
                const result = await fetch(url);
                console.log(result);
            } catch(e) {
                console.error(e);
            }
        }




    }

    const colorModeBtn = document.getElementById("color-mode-btn");
    colorModeBtn.addEventListener("click", evt => setColorMode(true));

    await setColorMode(false);
});
