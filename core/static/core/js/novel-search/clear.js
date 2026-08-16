const searchInput = document.querySelector('#novel-search-input')

document.querySelector('[data-clear-icon]')
    .addEventListener('click', (e) => { searchInput.value = '' })