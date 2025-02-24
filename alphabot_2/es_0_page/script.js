document.querySelectorAll(".button").forEach(button => {
    button.addEventListener("click", () => {
        console.log(button.textContent);
    });
});

document.addEventListener("keydown", (event) => {
    const key = event.key.toUpperCase();
    if (["W", "A", "S", "D"].includes(key)) {
        console.log(key);
    }
});