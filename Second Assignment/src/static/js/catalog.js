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
    // Get the product list container
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

    // Fetch the products based on the search term
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
                const productContainer = document.createElement('div');
                productContainer.classList.add('product-container');

                const productCard = document.createElement('div');
                productCard.classList.add('product-card');

                // Add a click event listener to the product card
                productCard.addEventListener('click', () => redirectToProductPage(product.id));

                const imgElement = document.createElement('img');
                imgElement.src = `/get_image/catalog/${product.id}.png`;
                imgElement.alt = product.name;
                productCard.appendChild(imgElement);

                productCard.innerHTML += `
                    <div class="product-content">
                        <h3>${product.name}</h3>
                        <p style="color: red">ID: ${product.id}</p>
                        <p class="price" style="color: green">${product.price} €</p>
                        <p class="product-description">${product.description}</p>
                    </div>
                `;

                const productButtonsContainer = document.createElement('div'); // Container for cart buttons
                productButtonsContainer.classList.add('product-buttons-container');

                // add a quantity input
                const quantityInput = document.createElement('input');
                quantityInput.type = 'number';
                quantityInput.min = 1;
                quantityInput.max = product.stock;
                quantityInput.value = 1;
                quantityInput.classList.add('quantity-input');

                const addToCartButton = document.createElement('button');
                addToCartButton.innerHTML = '<i class="fas fa-cart-plus"></i>'; // Font Awesome icon for "Add to Cart"
                addToCartButton.classList.add('cart-button');
                addToCartButton.addEventListener('click', (event) => {
                    event.stopPropagation();
                    product.quantity = 0;
                    product.quantity = parseInt(quantityInput.value);
                    if (product.quantity < 0) {
                        product.quantity = 0;
                    }
                    shoppingCart.addProduct(product);
                });

                const removeItemButton = document.createElement('button');
                removeItemButton.innerHTML = '<i class="fas fa-trash"></i>'; // Font Awesome icon for "Remove from Cart"
                removeItemButton.classList.add('cart-button');
                removeItemButton.addEventListener('click', (event) => {
                    event.stopPropagation();
                    product.quantity = 0;
                    product.quantity = parseInt(quantityInput.value);
                    if (product.quantity < 0) {
                        product.quantity = 0;
                    }
                    shoppingCart.removeProduct(product);
                });

                // Append the cart buttons to the container
                productButtonsContainer.appendChild(quantityInput);
                productButtonsContainer.appendChild(addToCartButton);
                productButtonsContainer.appendChild(removeItemButton);

                // Append the product card and cart buttons container to the product container
                // productContainer.appendChild(productCard);
                productCard.appendChild(productButtonsContainer);

                // Append the product container to the product list
                productList.appendChild(productCard);
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
fetch('/products')
    .then(response => response.json())
    .then(data => {
        const maxProductPrice = Math.max(...data.map(product => parseFloat(product.price)));
        initPriceSlider(maxProductPrice); // Initialize the slider with maxProductPrice
    })
    .catch(error => {
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
document.getElementById('logoutButton').addEventListener('click', function() {
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





