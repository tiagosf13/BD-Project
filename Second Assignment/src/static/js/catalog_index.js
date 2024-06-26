const productContainer = document.querySelector('.product-list');
const searchInput = document.getElementById('searchInput');
const categoryFilter = document.getElementById('categoryFilter');
const sortOrderSelect = document.getElementById('sortOrder');

const priceSlider = document.getElementById('priceSlider');
const minMaxPriceLabel = document.getElementById('minMaxPriceLabel');

// Function to update price labels based on the slider values
function updatePriceLabels() {
    const [minPrice, maxPrice] = priceSlider.noUiSlider.get();
    minMaxPriceLabel.textContent = `Price Range: ${minPrice} € - ${maxPrice} €`;
}


// Function to display products
function displayProducts() {
    const searchTerm = searchInput.value.toLowerCase();
    const selectedCategory = categoryFilter.value;
    const productList = document.querySelector('.product-list');

    // Create a payload object to send to the server
    const payload = {
        searchTerm: searchTerm,
        selectedCategory: selectedCategory,
        minPrice: parseFloat(priceSlider.noUiSlider.get()[0]),
        maxPrice: parseFloat(priceSlider.noUiSlider.get()[1]),
        inStock: true,
        sortOrder: sortOrderSelect.value
    };
    // Construct the query parameters
    const queryParams = new URLSearchParams(payload).toString();
    console.log(queryParams);

    // Fetch products from Flask route
    fetch(`/products?${queryParams}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            // Clear existing products
            productContainer.innerHTML = '';

            data.forEach(product => {
                const productCard = document.createElement('div');
                productCard.classList.add('product-card');

                // Add a click event listener to the product card
                productCard.addEventListener('click', () => redirectToProductPage(product.id));

                const imgElement = document.createElement('img');
                imgElement.src = `/get_image/catalog/${product.id}.png`;
                imgElement.alt = product.name;
                productCard.appendChild(imgElement);

                productCard.innerHTML += `
                <h3>${product.name}</h3>
                <p style="color: red">ID: ${product.id}</p>
                <p class="price" style="color: green">${product.price} €</p>
                <p class="product-details">${product.description}</p>
                `;

                productContainer.appendChild(productCard);
            });
        })
        .catch(error => {
            console.error('Error fetching products:', error);
        });
}


// Function to initialize the dual-handle slider
function initPriceSlider(maxProductPrice) {
    noUiSlider.create(priceSlider, {
        start: [0, maxProductPrice], // Set the initial range based on maxProductPrice
        connect: true,
        range: {
            'min': 0,
            'max': maxProductPrice
        }
    });

    // Event listener for the slider
    priceSlider.noUiSlider.on('update', () => {
        updatePriceLabels();
        displayProducts(); // Update products when the price range changes
    });
}

function redirectToProductPage(productId) {
    // Redirect to the product page with the product ID
    window.location.href = `/product/${productId}`;
}

// Call displayProducts once when the page loads
// Fetch products from Flask route
fetch(`/products/`, {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
    }
})
    .then(response => response.json())
    .then(data => {
        const maxProductPrice = Math.max(...data.map(product => parseFloat(product.price)));
        initPriceSlider(maxProductPrice); // Initialize the slider with maxProductPrice
    }).catch(error => {
        console.error('Error fetching products:', error);
    });


// Event listeners for filtering, searching, and sorting
searchInput.addEventListener('input', displayProducts);
categoryFilter.addEventListener('change', displayProducts);
sortOrderSelect.addEventListener('change', displayProducts);
categoryFilter.addEventListener('change', displayProducts);

function goToLogin() {

    // Redirect to the profile page
    window.location.href = "/login";
}

function goToSignUp() {

    // Redirect to the profile page
    window.location.href = "/signup";
}


// JavaScript to handle the logout button click
document.getElementById('logoutButton').addEventListener('click', function () {
    // Send a request to the logout route
    fetch('/logout', {
        method: 'GET',
        credentials: 'same-origin',  // Include cookies in the request
    })
        .then(response => {
            if (response.ok) {
                // Redirect to the login or home page after successful logout
                window.location.href = '/';  // Replace with your actual login or home page URL
            }
        })
        .catch(error => {
            console.error('Error logging out:', error);
        });
});

