const chapterListButton = document.querySelector("[data-chapter-list-modal-button]");
const settingsModal = document.querySelector("[data-chapter-list-modal]");
const closeButton = document.querySelector("[data-chapter-list-modal-close]");

closeButton.addEventListener("input", () => chapterListButton.hidden = true);