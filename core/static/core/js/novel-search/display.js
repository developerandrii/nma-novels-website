const novelSearch = document.querySelector('[data-novel-search]')
const novelSearchDisplay = document.querySelector('[data-novel-search-display]')
const novelSearchClose = document.querySelector('[data-novel-search-close]')

novelSearchDisplay.addEventListener("click", () => {
    novelSearch.classList.remove('novel-search--hidden');
    searchInput.focus();
})

novelSearchClose.addEventListener("click", () => {
    novelSearch.classList.add('novel-search--hidden')
});





