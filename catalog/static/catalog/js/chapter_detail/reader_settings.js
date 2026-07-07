const settingsButton = document.querySelector("[data-reader-settings-modal-button]");
const settingsModal = document.querySelector("[data-reader-settings-modal]");
const closeButton = document.querySelector("[data-reader-settings-modal-close]");
const resetButton = document.querySelector("[data-reader-reset]");

// Modal Controls
settingsButton.addEventListener("click", () => settingsModal.hidden = false);
closeButton.addEventListener("click", () => settingsModal.hidden = true);

// Reader Configurations
const fontSizeInput = document.querySelector("[data-reader-font-size]");
const paragraphSpacingInput = document.querySelector("[data-reader-paragraph-spacing]");
const lineHeightInput = document.querySelector("[data-reader-linke-height]");


// Take settings from localstorage  
if (localStorage.getItem("--reader-font-size")) { 
    document.documentElement.style.setProperty("--reader-font-size", `${localStorage.getItem("--reader-font-size")}`);
    fontSizeInput.value = localStorage.getItem("--reader-font-size");
}
if (localStorage.getItem("--reader-paragraph-spacing")) { 
    document.documentElement.style.setProperty("--reader-paragraph-spacing", `${localStorage.getItem("--reader-paragraph-spacing")}`);
    paragraphSpacingInput.value = localStorage.getItem("--reader-paragraph-spacing");
}
if (localStorage.getItem("--reader-linke-height")) { 
    document.documentElement.style.setProperty("--reader-linke-height", `${localStorage.getItem("--reader-linke-height")}`);
    lineHeightInput.value = localStorage.getItem("--reader-linke-height");
}


// Change reader settings
fontSizeInput.addEventListener("input", () => {
    document.documentElement.style.setProperty("--reader-font-size", `${fontSizeInput.value}`);
    localStorage.setItem("--reader-font-size", `${fontSizeInput.value}`)
});

paragraphSpacingInput.addEventListener("input", () => {
    document.documentElement.style.setProperty("--reader-paragraph-spacing", `${paragraphSpacingInput.value}`);
    localStorage.setItem("--reader-paragraph-spacing", `${paragraphSpacingInput.value}`)
});

lineHeightInput.addEventListener("input", () => {
    document.documentElement.style.setProperty("--reader-linke-height", `${lineHeightInput.value}`);
    localStorage.setItem("--reader-linke-height", `${lineHeightInput.value}`)
});

// Reset functionality
resetButton.addEventListener("click", () => {
    // default values
    fontSizeInput.value = `16px`;
    paragraphSpacingInput.value = `16px`;
    lineHeightInput.value = `1.3`;

    document.documentElement.style.setProperty("--reader-font-size", `${fontSizeInput.value}`);
    document.documentElement.style.setProperty("--reader-paragraph-spacing", `${paragraphSpacingInput.value}`);
    document.documentElement.style.setProperty("--reader-linke-height", `${lineHeightInput.value}`);
    
    localStorage.removeItem("--reader-font-size")
    localStorage.removeItem("--reader-paragraph-spacing")
    localStorage.removeItem("--reader-linke-height")
});

