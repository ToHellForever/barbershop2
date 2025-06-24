console.log('Страница загружена');
// чтобы год отображался автоматически
document.addEventListener("DOMContentLoaded", function() {
    var yearElement = document.getElementById("current-year");
    if (yearElement) {
        var currentYear = new Date().getFullYear();
        yearElement.textContent = currentYear;
    }
});