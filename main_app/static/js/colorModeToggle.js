/**
 * File: colorModeToggle.js
 * Frontend script
 * Used by dark/light mode button in the navbar.html template
 * Handles toggling color mode, sets the theme and saves to localstorage/backend
 *
 * Requirements:
 * - Bootstrap 5 and Bootstrap icons loaded in template
 * - button (of any element type) with id: "color-mode-btn"
 * - api pathway /api/color-mode/<str:mode>/ sets theme to backend user
 * - "data-guest" attribute in <html> tag
 *
 * Comment:
 * This script would be better encapsulated in a component like React*
 */

// encapsulate in module for clean global namespace
(function() {

    // driver code
    window.addEventListener("load", () => {
        // get button element
        const colorModeBtn = document.getElementById("color-mode-btn");

        // button click behavior
        colorModeBtn.addEventListener("click", () => {
            setColorMode(true);
            setColorModeIcon(colorModeBtn, getColorMode());
        });

        // apply color mode & set icon at page load
        setColorMode(false);
        setColorModeIcon(colorModeBtn, getColorMode());
    });


    /**
     * Get currently applied color theme / mode from the html element
     * @returns {string}
     */
    function getColorMode() {
        return document.querySelector("html").getAttribute("data-bs-theme");
    }


    /**
     * Apply the color mode and save it in local storage / database.
     * Checks these places in this order for color mode setting:
     *  1. user settings theme
     *  2. local storage
     *  3. default to "light"
     *
     * Thereafter, local storage will be set, as well as the user setting
     * if there is a user logged in.
     *
     * @param flip {boolean} whether to toggle "light"/"dark", default: `false`
     * @returns {Promise<boolean>}
     */
    async function setColorMode(flip = false) {
        const html = document.querySelector("html");

        // Get mode
        // try getting from html attribute (pre-set if user logged in)
        let mode = html.getAttribute("data-bs-theme");
        if (!mode) // if not available, check cookies
            mode = getCookies().get("color_mode");
        if (!mode) // if not available, default to light
            mode = "light";

        if (flip)
            mode = (mode === "light") ? "dark" : "light";

        // apply the mode to the html element (a catch-all if it wasn't set before)
        html.setAttribute("data-bs-theme", mode);

        // save mode
        // set color_mode cookie, expires in one year
        const yearFromNow = new Date;
        yearFromNow.setFullYear(yearFromNow.getFullYear() + 1);
        document.cookie = "color_mode=" + mode + "; expires=" + yearFromNow + "; path=/;";

        // if a user is logged in, save mode to their profile settings
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


    /**
     * Set the color-mode button icon depending on mode
     * @param btnEl {HTMLElement} button element
     * @param mode {string} e.g. "light" or "dark"
     */
    function setColorModeIcon(btnEl, mode) {
        // set the icon class name based on the mode
        const iconClass = "bi " + (mode === "light") ? "bi-sun-fill" : "bi-moon-stars-fill";
        btnEl.innerHTML = `<i class='${iconClass}'></i>`;

        // set any iframe background color if any are present
        document.getElementsByName("iframe").forEach(iframe => {
            iframe.style.background = (mode === "light") ? "#FEFEFE" : "#222";
        });
    }

})();


