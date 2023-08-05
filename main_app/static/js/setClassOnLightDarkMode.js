/**
 * Based on color-mode, set a list of HTMLElements with `ids` to
 * a class in light mode or dark mode.
 *
 * @param elementIds {string[]} list of target element id's
 * @param darkModeClass {string} class name to set when dark mode
 * @param lightModeClass {string} class name to set when light mode
 */
function setClassOnLightDarkMode(elementIds, darkModeClass, lightModeClass) {
    const modeBtnEl = document.getElementById('color-mode-btn');
    if (!modeBtnEl) return; // no mode button available


    // get elements from ids
    const els = [];
    elementIds.forEach(id => {
        const btn = document.getElementById(id);
        if (btn)
            els.push(btn);
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