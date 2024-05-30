import random, os
from datetime import datetime
from handlers.Retrievers import get_product_by_id, get_current_dir
from handlers.DataBaseCoordinator import db_query


def verify_product_exists(product_name):

    # Secure Query: Check if the ID exists in the specified table
    query = "SELECT product_id FROM products WHERE product_name = ?;"
    results = db_query(query, (product_name))

    if len(results) == 0:
        return False
    else:
        return True

def check_product_availability(product_id):

    # Secure Query: Check if the ID exists in the specified table
    query = "SELECT available FROM products WHERE product_id = ?;"
    results = db_query(query, (product_id))

    return results[0][0] if results else False


def verify_id_exists(id, table):

    # Secure Query: Check if the ID exists in the specified table
    if table == "products":
        query = "SELECT product_id FROM products WHERE product_id = ?;"
    elif table == "reviews":
        query = "SELECT product_id FROM reviews WHERE review_id = ?;"
    elif table == "orders":
        query = "SELECT user_id FROM orders WHERE order_id = ?;"
    
    results = db_query(query, (id))

    if len(results) == 0:
        return False
    else:
        return True
    

def generate_random_product_id(table):

    # Generate a random ID
    random_id = random.randint(100000, 999999)

    # Check if the generated ID already exists, regenerate if necessary
    while verify_id_exists(random_id, table):
        random_id = random.randint(100000, 999999)

    return random_id


def create_product_image(id, product_photo):

    try:
        # Define the path for the product image directory
        product_image_directory = os.path.join(get_current_dir(), "catalog")

        # Create the product image directory and any missing parent directories
        os.makedirs(product_image_directory, exist_ok=True)

        # Construct the full path for the product image file
        product_image_path = os.path.join(product_image_directory, f"{id}.png")

        # Check if the product image file already exists and remove it
        if os.path.exists(product_image_path):
            os.remove(product_image_path)

        # Save the product photo to the specified path
        product_photo.save(product_image_path)
    except Exception as e:
        print(e)  # Handle or log any exceptions that occur during this process


def create_product(product_name, product_description, product_price, product_category, product_quantity, product_photo):

    # check if the product already exists
    if verify_product_exists(product_name):
        return None
    else:
        # Generate a unique user id
        product_id = str(generate_random_product_id("products"))
        
        # Add the user to the users table
        db_query(
                "INSERT INTO products (product_id, product_name, product_description, price, category, stock, available) \
                VALUES (?, ?, ?, ?, ?, ?, ?);",
                (product_id, product_name, product_description, product_price, product_category, product_quantity, True)
        )

        # Create a folder for the user
        create_product_image(product_id, product_photo)

        # Return the created user
        return product_id


def remove_product(id):

    # Secure Query to delete the product from the carts
    ## TODO transformar em Procedure com transaction
    query = """
        DELETE FROM carts WHERE product_id = ?;
        UPDATE products SET available = 0 WHERE product_id = ?;
    """
    db_query(query, (id, id))
    return True

def remove_product_from_cart(id, user_id):
    # Secure Query to delete the product from the carts
    query = "DELETE FROM carts WHERE product_id = ? AND user_id = ?;"
    db_query(query, (id, user_id))
    return True

def remove_all_products_from_cart(user_id):
    # Secure Query to delete the product from the carts
    query = "DELETE FROM carts WHERE user_id = ?;"
    db_query(query, (user_id))
    return True

def get_cart_quantity(id, product_id):
    query = "SELECT quantity FROM carts WHERE user_id = ? AND product_id = ?"
    quantity = db_query(query, (id, product_id))
    
    return quantity[0][0] if len(quantity) > 0 else 0


def set_cart_item(id, product_id, quantity, operation):

    # Secure Query: Check if the product is already in the cart
    query = "SELECT * FROM carts WHERE product_id = ? AND user_id = ?"
    results = db_query(query, (product_id, id))

    if len(results) != 0:
        # Update the quantity
        if operation == "add":
            # Secure Query: Update the quantity
            update_query = "UPDATE carts SET quantity = quantity + ? WHERE product_id = ? AND user_id = ?"
        else:
            # Secure Query: Update the quantity
            update_query = "UPDATE carts SET quantity = quantity - ? WHERE product_id = ? AND user_id = ?"

        # Secure Query: Execute the update
        db_query(update_query, (quantity, product_id, id))
        return True
    else:
        # Add the product to the cart
        # Secure Query: Insert into the cart
        insert_query = "INSERT INTO carts (product_id, quantity, user_id) VALUES (?, ?, ?)"
        db_query(insert_query, (product_id, quantity, id))
        return True

def create_review(id, user_id, review, rating):
    review_id = str(generate_random_product_id("reviews"))

    # Secure Query
    query = "INSERT INTO reviews (review_id, product_id, user_id, review_text, rating, review_date) VALUES (?, ?, ?, ?, ?, ?);"
    db_query(query, (review_id, id, user_id, review, rating, datetime.now()))

    return True


def register_order(user_id, order_details, products):
    try:
        products_to_register = {}
        total_price = 0
        for product in products:
            total_price += float(product["price"]) * product["quantity"]
            products_to_register[product["product_id"]] = product["quantity"]

        order_id = str(generate_random_product_id("orders"))
        time = datetime.now()
        
        
        query = """
            INSERT INTO orders (order_id, user_id, total_price, shipping_address, order_date) VALUES (?, ?, ?, ?, ?);
        """
        db_query(query, (order_id, user_id, total_price, order_details["shipping_address"], time))
        
        # Register in all orders
        # Secure Query
        for product in products:
            query = """
                INSERT INTO products_ordered (order_id, product_id, quantity) VALUES (?, ?, ?);
            """
            db_query(query, (order_id, product["product_id"], product["quantity"]))

        return True, order_id
    except:
       return False, None
    

def update_product_after_order(products):

    for product in products:
        product_stock = get_product_by_id(product["product_id"])["stock"]
        quantity = product["quantity"]
        if product_stock < quantity:
            return False
        # update the product quantity
        update_product( {
            "productID" : int(product["product_id"]),
            "productQuantity": product_stock - quantity,
        })
    return True

def update_product(updatedProduct: dict):
    query = "exec updateProduct"
    params = []

    for key, value in updatedProduct.items():
        if value is not None and value != '':
            query = f"{query} @{key}=?,"
            params.append(value)
    # Remove last comma
    query = query[:-1]

    db_query(query=query, params=params)
