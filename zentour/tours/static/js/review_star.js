document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll(".star");
    const hiddenInput = document.querySelector('input[name="rating"]');

    stars.forEach((star, index) => {
        star.addEventListener("click", function () {
            const rating = index + 1;
            hiddenInput.value = rating;
            highlightStars(rating);
        });
    });

    function highlightStars(rating) {
        stars.forEach((star, index) => {
            if (index < rating) {
                star.classList.add("checked");
            } else {
                star.classList.remove("checked");
            }
        });
    }
});