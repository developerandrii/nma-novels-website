const chapterListButton = document.querySelector("[data-chapter-list-button]");
const chapterListModal = document.querySelector("[data-chapter-list-modal]");
const closeChapterListButton = document.querySelector("[data-chapter-list-modal-close]");

chapterListButton.addEventListener("click", () => chapterListModal.hidden = false)
closeChapterListButton.addEventListener("click", () => chapterListModal.hidden = true);