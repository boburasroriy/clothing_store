document.addEventListener("DOMContentLoaded", () => {
    console.log("Apple-style Clothing Store Loaded");

   
    document.querySelectorAll(".table tbody tr").forEach(row => {
        row.addEventListener("mouseenter", () => row.style.backgroundColor = "#f0f8ff");
        row.addEventListener("mouseleave", () => row.style.backgroundColor = "");
    });
});
