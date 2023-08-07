/**
 * Based on color-mode, set a list of HTMLElements with `ids` to
 * a class in light mode or dark mode.
 *
 * @param elementQueries {string[]} list of target element querySelector values
 * @param darkModeClass {string} class name to set when dark mode
 * @param lightModeClass {string} class name to set when light mode
 */
function setClassOnLightDarkMode(elementQueries, darkModeClass, lightModeClass) {
    const modeBtnEl = document.getElementById('color-mode-btn');
    if (!modeBtnEl) return; // no mode button available


    // get elements from ids
    const els = [];
    elementQueries.forEach(query => {
        const subEls = document.querySelectorAll(query);
        subEls.forEach(el => els.push(el));
    });


    // theme change callback
    const handleThemeChange = () => {
        if (!els.length) return;

        const theme = document.documentElement.getAttribute('data-bs-theme');
        if (!theme) return; // in case the theme was not set, do not make change

        // set the class based on the current theme
        if (theme === "dark") {    // on dark mode
            els.forEach(el => {
                if (darkModeClass)
                    el.classList.add(darkModeClass);
                if (lightModeClass)
                    el.classList.remove(lightModeClass);
            });
        } else {                   // on light mode
            els.forEach(el => {
                if (lightModeClass)
                    el.classList.add(lightModeClass);
                if (darkModeClass)
                    el.classList.remove(darkModeClass);
            });
        }
    };

    // set the classes once onload
    handleThemeChange();

    // and every time the light/dark mode button is clicked
    modeBtnEl.addEventListener('click', handleThemeChange);
}