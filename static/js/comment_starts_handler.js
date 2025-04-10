// Starts on product comments handler
const stars = document.querySelectorAll('.star');
const ratingInput = document.getElementById('rating-input');
let selectedValue = 0;


stars.forEach(star => {
    star.addEventListener('mouseover', () => {
        const value = parseInt(star.getAttribute('data-value'));
        highlightStars(value);
    });

    star.addEventListener('mouseout', () => {
        highlightStars(selectedValue);
    });

    star.addEventListener('click', () => {
        selectedValue = parseInt(star.getAttribute('data-value'));
        ratingInput.value = selectedValue;
        highlightStars(selectedValue);
    });
});

function highlightStars(value) {
    stars.forEach(star => {
        const starValue = parseInt(star.getAttribute('data-value'));
        if (starValue <= value) {
            star.classList.add('hovered');
        } else {
            star.classList.remove('hovered');
        }
    });
}