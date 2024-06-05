const reorderButtons = document.querySelectorAll('.reorderButton');
reorderButtons.forEach(button => {
    button.addEventListener('click', function () {
        const productDetails = this.getAttribute('data-product');
        console.log('Product Details:', productDetails);
        try {
            const parsedProductDetails = JSON.parse(productDetails);
            reorder_item(parsedProductDetails);
        } catch (error) {
            console.error('Error parsing JSON:', error);
        }
    });
});

async function reorder_item(product) {
    try {
        const response = await fetch(`/add_item_cart/${product.product_id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ quantity: product.quantity }), // You can adjust the quantity here
        });

        if (response.ok) {
            // Call a function to update the cart display
            updateCartDisplay();

        } else {
            product.quantity = 0;
            // get the error message from the response,
            const errorMessage = await response.json();
            // then display it on the page
            alert('Failed to add product to the cart. ' + errorMessage.error);
            // Handle errors or server responses here
            console.error('Failed to add product to the cart.');
        }
    } catch (error) {
        console.error('Error adding product to the cart:', error);
    }
}


var acc = document.getElementsByClassName("accordion");
var i;
for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    /* Toggle between adding and removing the "active" class,
    to highlight the button that controls the panel */
    this.classList.toggle("active");

    /* Toggle between hiding and showing the active panel */
    var panel = this.nextElementSibling;
    if (panel.style.display === "block") {
      panel.style.display = "none";
    } else {
      panel.style.display = "block";
    }

    if (panel.style.maxHeight) {
        panel.style.maxHeight = null;
      } else {
        panel.style.maxHeight = panel.scrollHeight + "px";
      }
  });
}
// Open first Accordion
window.onload = () => {
    firstAccordion = document.getElementsByClassName("accordion")[0]
    if (firstAccordion == null) {
        return;
    }
    firstAccordion.classList.add("active");
    firstPanel = firstAccordion.nextElementSibling;
    firstPanel.style.display = "block"
    firstPanel.style.maxHeight = firstPanel.scrollHeight + "px";
}