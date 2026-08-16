const chapterListButton = document.querySelector("[data-chapter-list-button]");
const chapterListModal = document.querySelector("[data-chapter-list-modal]");
const closeChapterListButton = document.querySelector("[data-chapter-list-modal-close]");
const currentChapter = document.querySelector('[data-current-chapter]')

chapterListButton.addEventListener("click", () => {
    chapterListModal.hidden = false;
    currentChapter.scrollIntoView({
        block: 'center',
        behavior: 'instant'
    })
})
closeChapterListButton.addEventListener("click", () => chapterListModal.hidden = true);