// Will be loaded globally in all template files

window.addEventListener("load", evt => {
    // Prevent forms from being submitted multiple times
    const forms = document.querySelectorAll("form");
    for (let i = 0; i < forms.length; ++i) {
        const form = forms[i];
        form.addEventListener("submit", evt => {
            if (form.dataset["attempted"])
                evt.preventDefault();
            else
                form.dataset["attempted"] = "true";
        });
    }
});
