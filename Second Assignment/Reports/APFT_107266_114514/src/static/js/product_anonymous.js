// Function to fetch reviews and ratings and populate the review list and average rating
function fetchReviewsAndRating() {

    fetch(`/get_reviews/${productId}`)
        .then(response => response.json())
        .then(data => {
            // Clear existing reviews
            const reviewList = document.getElementById('reviewList');
            reviewList.innerHTML = '';

            data.forEach(review => {
                displayReview(review);
            });
        })
        .catch(error => {
            console.error('Error fetching reviews and ratings:', error);
        });
}

// Call the function after the page has loaded
document.addEventListener('DOMContentLoaded', function() {
    fetchReviewsAndRating();
});


// Add an event listener to the "Back to Catalog" link
document.getElementById('backToCatalog').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default link behavior
    history.go(-1); // Go back to the previous page
});


// Function to display a review in the review list
function displayReview(review) {
    const reviewList = document.getElementById('reviewList');
    const listItem = document.createElement('li');
    listItem.classList.add('review-balloon'); // Add a class for styling

    listItem.innerHTML = `
        <strong>${review.username}</strong> - ${review.rating} ★<br>
        <p class="review-paragraph">${review.review}</p>
    `;

    reviewList.appendChild(listItem);
}