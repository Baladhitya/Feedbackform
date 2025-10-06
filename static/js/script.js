$(document).ready(function() {
    $('#feedbackForm').on('submit', function(e) {
        let valid = true;
        // Clear previous errors
        $('.error-message').text('');

        // Name validation
        const name = $('#name').val().trim();
        if (name.length < 2) {
            $('#nameError').text('Name must be at least 2 characters.');
            valid = false;
        }

        // Email validation
        const email = $('#email').val().trim();
        const emailPattern = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
        if (!emailPattern.test(email)) {
            $('#emailError').text('Please enter a valid email address.');
            valid = false;
        }

        // Feedback validation
        const feedback = $('#feedback').val().trim();
        if (feedback.length < 5) {
            $('#feedbackError').text('Feedback must be at least 5 characters.');
            valid = false;
        }

        // Rating validation
        const rating = $('#rating').val();
        if (!rating) {
            $('#ratingError').text('Please select a rating.');
            valid = false;
        }

        // Recommend validation
        const recommend = $('input[name="recommend"]:checked').val();
        if (!recommend) {
            $('#recommendError').text('Please select Yes or No.');
            valid = false;
        }

        if (!valid) {
            e.preventDefault();
        }
    });
});
