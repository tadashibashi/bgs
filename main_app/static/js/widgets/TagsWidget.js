// This script handles tag input in games/form.html

window.addEventListener("load", tagFormatterMain);




function tagFormatterMain() {
    // Add form-control class to each input
    document.querySelectorAll("form input, textarea").forEach(input => {
        input.classList.add("form-control");
    });

    // Hide <input> and use an editable div to display
    const tagInputEl = document.getElementById("id_tags");
    tagInputEl.hidden = true;

    const editableEl = document.createElement("div");

    editableEl.setAttribute("contenteditable", "true");
    editableEl.setAttribute("class", "tag-input form-control");

    function formatTags(evt) {
        const text = editableEl.innerText;
        let html = "";
        const tags = text.split(/\s*[\s,]\s*/);
        for (let i = 0; i < tags.length; ++i) {
            const tag = tags[i].trim();
            if (i < tags.length - 1) {
                if (tag) {
                    html += "<span class='tag'>" + tag + "</span>&nbsp";
                }
            } else {
                html += "<span>" + tag + "</span>";
            }
        }

        return html;
    }

    function repositionCursorAndApplyHtml(html) {
        // Move cursor back to last position
        editableEl.focus();
        const sel = window.getSelection();//get the selection object (allows you to change selection)
        let focusOffset = sel.focusOffset;

        let _pos;
        {
            let found = false;
            _pos = 0;
            for (let i = 0; i < editableEl.childNodes.length; ++i) {
                const cur = editableEl.childNodes[i];
                if (cur.contains(sel.focusNode)) {
                    found = true;
                    break;
                } else {
                    ++_pos;
                }
            }

            if (!found)
                _pos = -1;
        }

        const lastSize = editableEl.childNodes.length;

        editableEl.innerHTML = html; // finally set the div's html
        let curSize = editableEl.childNodes.length;
        let curNode = editableEl.childNodes[_pos + Math.max(curSize - lastSize, 0)];
        if (!curNode)
            curNode = editableEl.childNodes[_pos];
        if (!curNode)
            curNode = editableEl;

        if (curNode.childNodes.length)
            curNode = curNode.childNodes[0];
        else if (focusOffset === 2)
            curNode = editableEl.childNodes[_pos + Math.max(curSize - lastSize, 0) + 1];

        const newSel = document.getSelection()
        newSel.collapse(curNode, focusOffset);
        newSel.collapseToEnd();
    }

    editableEl.addEventListener("click", evt => {
        if (!evt.target.classList.contains("after")) return;

        editableEl.removeChild(evt.target.parentElement);
    });

    // Automatically format tags nicely.
    // TODO Icebox: it's hard to get the caret to jump to the correct position.
    // Prevent the cursor from moving into the tags
    editableEl.addEventListener("input", evt => {
        repositionCursorAndApplyHtml(formatTags());
    });
    editableEl.innerText = window["game-tags"];
    console.log(window["game-tags"]);
    editableEl.innerHTML = formatTags();

    // Transfer div innerText to the actual input on submission
    const submitEl = document.querySelector("button[type='submit']");
    submitEl.onclick = function(evt) {
        tagInputEl.value = editableEl.innerText;
    }

    tagInputEl.parentElement.append(editableEl);

    window.removeEventListener("load", tagFormatterMain);
}

