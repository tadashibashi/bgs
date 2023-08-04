// This script handles tag input in games/form.html

// use module to encapsulate code from global namespace
(function() {
    window.addEventListener("load", main);

    // driver code
    function main() {

        // Hide <input> and use an editable div to display
        const tagInputEl = document.getElementById("id_tags");
        tagInputEl.hidden = true;

        const editableEl = document.createElement("div");

        editableEl.setAttribute("contenteditable", "true");
        editableEl.setAttribute("class", "tag-input form-control");

        function formatTags(editableEl) {
            let html = "";
            const tags = editableEl.innerText.split(/\s*[\s,]\s*/);

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

        /**
         * Helper to set html string to the contenteditable area and reposition
         * the cursor after the html has been set.
         * @param html {string}
         * @param editableEl {HTMLDivElement} div with contenteditable set
         */
        function repositionCursorAndApplyHtml(html, editableEl) {
            // make sure contenteditable area is focused
            editableEl.focus();

            const sel = window.getSelection();

            // get position offset
            let focusOffset = sel.focusOffset;

            // get node offset
            let nodeOffset;
            {
                let found = false;
                nodeOffset = 0;
                for (let i = 0; i < editableEl.childNodes.length; ++i) {
                    const cur = editableEl.childNodes[i];
                    if (cur.contains(sel.focusNode)) {
                        found = true;
                        break;
                    } else {
                        ++nodeOffset;
                    }
                }

                if (!found)
                    nodeOffset = -1;
            }

            const lastSize = editableEl.childNodes.length;

            // Get the node, making adjustments for edge-cases
            editableEl.innerHTML = html; // finally set the div's html
            let curSize = editableEl.childNodes.length;
            let curNode = editableEl.childNodes[nodeOffset + Math.max(curSize - lastSize, 0)];
            if (!curNode)
                curNode = editableEl.childNodes[nodeOffset];
            if (!curNode)
                curNode = editableEl;

            if (curNode.childNodes.length)
                curNode = curNode.childNodes[0];
            else if (focusOffset === 2)
                curNode = editableEl.childNodes[nodeOffset + Math.max(curSize - lastSize, 0) + 1];

            // done, make selection
            const newSel = document.getSelection()
            newSel.collapse(curNode, focusOffset);
            newSel.collapseToEnd();
        }


        editableEl.addEventListener("click", evt => {
            if (!evt.target.classList.contains("after")) return;

            editableEl.removeChild(evt.target.parentElement);
        });

        // Automatically format tags nicely
        // TODO: Try to fix caret jumping to wrong position
        // It's hard to get the caret to jump to the correct position
        // Prevent the cursor from moving into the tags when at offset 2
        editableEl.addEventListener("input", evt =>
            repositionCursorAndApplyHtml(formatTags(editableEl), editableEl));

        // Set and format the initial game tags onload
        editableEl.innerText = window["game-tags"];
        editableEl.innerHTML = formatTags(editableEl);

        // Transfer div innerText to the actual input on submission
        const submitEl = document.querySelector("button[type='submit']");
        submitEl.onclick = () => tagInputEl.value = editableEl.innerText;

        tagInputEl.parentElement.append(editableEl);

        window.removeEventListener("load", main);
    }

})();

