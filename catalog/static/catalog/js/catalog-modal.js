const catalogModal = document.querySelector('[data-catalog-modal]');
const catalogButton = document.querySelector('[data-catalog-button]');

catalogButton.addEventListener("click", (e)=> {
    e.stopPropagation()
    catalogModal.hidden = false
});

document.body.addEventListener("click", () => catalogModal.hidden = true);