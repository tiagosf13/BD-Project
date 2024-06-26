// Function to fetch reviews and ratings and populate the review list and average rating
function fetchReviewsAndRating() {

    fetch(`/get_reviews/${productId}`)
        .then(response => response.json())
        .then(data => {
            // Clear existing reviews
            const reviewList = document.getElementById('reviewList');
            reviewList.innerHTML = '';

            // Display reviews  
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


// Function to add a user review
function addReview(event) {
    event.preventDefault(); // Prevent the default form submission

    // Collect form data
    const userReview = document.getElementById('userReview').value;
    const rating = parseInt(document.getElementById('rating').value);

    if (!userReview || isNaN(rating)) {
        alert('Please provide a review and rating.');
        return;
    }

    const formData = new FormData();
    formData.append('userReview', userReview);
    formData.append('rating', rating);

    // Send a POST request to the server
    fetch(`/add_review/${productId}`, {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (response.ok) {
            return response.json(); // Parse JSON if response is OK
        } else if (response.status === 403) {
            return response.json().then(data => { throw new Error(data.message); }); // Extract error message
        } else {
            throw new Error('Something went wrong');
        }
    })
    .then(data => {
        // Assuming the server responds with data, you can handle it here
        // For example, you can display a success message or update the review list

        // Clear the review and reset the rating
        document.getElementById('userReview').value = '';
        document.getElementById('rating').value = '1';

        // Refresh the average rating
        fetchReviewsAndRating();

        // Handle successful review submission
        alert(data.message); // Display success message
    })
    .catch(error => {
        console.error('Error adding review:', error);
        alert(error + "\nYou can only review a product you bought."); // Display error message
    });
}

// Function to display a review in the review list
function displayReview(review) {
    const reviewList = document.getElementById('reviewList');
    const listItem = document.createElement('li');
    listItem.classList.add('review-balloon'); // Add a class for styling

    listItem.innerHTML = `
        <strong>${review.username}</strong> ${review.rating} ★<br>
        <p class="review-paragraph">${review.review}</p><br>
        <small class="review-date">${review.review_date}</small>
    `;

    // Insert the new review at the beginning of the list
    reviewList.insertBefore(listItem, reviewList.firstChild);
}

// Add an event listener to the form submission
document.getElementById('reviewForm').addEventListener('submit', addReview);

document.getElementById('addToCart').addEventListener('click', function(event) {
    event.stopPropagation();
    const product = JSON.parse(productJSON); // Parse the JSON string back to an object
    const quantityInput = document.getElementById('quantity');
    product.quantity = parseInt(quantityInput.value);;
    if (product.quantity < 0) {
        product.quantity = 0;
    }
    // Now, you can use the 'product' object as needed
    shoppingCart.addProduct(product);
});


document.getElementById('removeFromCart').addEventListener('click', function(event) {
    event.stopPropagation();
    const product = JSON.parse(productJSON); // Parse the JSON string back to an object
    const quantityInput = document.getElementById('quantity');
    product.quantity = parseInt(quantityInput.value);;
    if (product.quantity < 0) {
        product.quantity = 0;
    }
    shoppingCart.removeProduct(product);
});

