const chapterPicker = document.querySelector("[data-chapter-picker]");

if (chapterPicker) {
    const button = chapterPicker.querySelector("[data-chapter-picker-button]");
    const list = chapterPicker.querySelector("[data-chapter-picker-list]");

    button.addEventListener("click", function () {
        const isOpen = button.getAttribute("aria-expanded") === "true";

        button.setAttribute("aria-expanded", String(!isOpen));
        list.hidden = isOpen;
    });

    document.addEventListener("click", function (event) {
        if (!chapterPicker.contains(event.target)) {
            console.log(event.target)
            button.setAttribute("aria-expanded", "false");
            list.hidden = true;
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            button.setAttribute("aria-expanded", "false");
            list.hidden = true;
        }
    });
}