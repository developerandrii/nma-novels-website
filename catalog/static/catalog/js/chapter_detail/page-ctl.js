let lastTapTime = 0;
const TAP_DELAY_THRESHOLD = 200; // Time in milliseconds


const pageCtl = document.querySelector("[data-page-ctl]");

// Use 'pointerdown'—it handles both desktop mice and mobile touch screens perfectly
window.addEventListener("click", (event) => {
    // SECURITY GUARD: If the user double-clicks inside a button, input, or link, STOP.
    if (event.target.closest("input") || event.target.closest("button") || event.target.closest("a")) {
        return;
    }
    const currentTime = Date.now();
    const timeSinceLastTap = currentTime - lastTapTime;
    
    if (timeSinceLastTap < TAP_DELAY_THRESHOLD && timeSinceLastTap > 0) {
        pageCtl.style.display = pageCtl.style.display == '' || pageCtl.style.display == 'flex'? 'none' : 'flex';
        // Reset the clock so a 3rd rapid tap doesn't immediately count as another double-tap
        lastTapTime = 0; 
    } else {
        // Record the time of this first click
        lastTapTime = currentTime;
    }
});