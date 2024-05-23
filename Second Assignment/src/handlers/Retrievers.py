import os
from handlers.DataBaseCoordinator import db_query


def get_current_dir():

    if os.name == "nt":
        # Get the current working directory
        current_directory = os.path.dirname(os.path.abspath(__file__)).split("\\handlers")[0]
    else:
        # Get the current working directory
        current_directory = os.path.dirname(os.path.abspath(__file__)).split("/handlers")[0]

    return current_directory



def get_all_products():
    # Secure Query - Select specific columns
    query = "SELECT product_id, product_name, product_description, price, category, stock, available FROM products"
    results = db_query(query)
    
    # Fetch all rows in one go and convert to a list of dictionaries
    products = [{
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "price": row[3],
        "category": row[4],
        "stock": row[5]
    } for row in results if row[6] == True]
    
    return products

def verify_product_id_exists(id):
    # Secure Query
    query = "SELECT product_name FROM products WHERE product_id = ?"
    results = db_query(query, (id))

    if len(results) == 0:
        return False
    else:
        return True
    

def get_product_by_id(id):
    # Secure Query
    query = "SELECT * FROM products WHERE product_id = ?"
    results = db_query(query, (id))


    if len(results) == 0:
        return None
    else:
        row = results[0]
        product = {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "price": row[3],
            "category": row[4],
            "stock": row[5],
            "available" : row[6]
        }
        return product
    

def get_product_reviews(product_id):

    # check if the product exists
    if not verify_product_id_exists(product_id):
        return None

    # Secure Query
    query = "SELECT * FROM reviews WHERE product_id = ?;"
    results = db_query(query, (product_id))

    reviews = []
    for row in results:
        review = {
            "review_id": row[0],
            "product_id": row[1],
            "user_id": row[2],
            "rating": row[3],
            "review": row[4],
            "review_date": row[5]
        }
        reviews.append(review)

    return reviews


def check_product_availability(product_id):

    # Secure Query: Check if the ID exists in the specified table
    query = "SELECT available FROM products WHERE product_id = ?;"
    results = db_query(query, (product_id))

    return results[0][0] if results else False


def get_cart(user_id):

    query = """
        SELECT products.product_id, quantity, products.product_name, products.price
        FROM carts
        JOIN products ON carts.product_id = products.product_id
        WHERE user_id=?
        ;
    """
    result = db_query(query, (user_id))

    cart = []

    for element in result:
        if not (check_product_availability(element[0]) and element[1] > 0 and element[1] <= get_product_by_id(element[0])["stock"]):
            delete_query = "DELETE FROM carts WHERE product_id = ? AND user_id = ?;"
            db_query(delete_query, (element[0], user_id))

        else:
            cart.append({
                "product_id": element[0],
                "quantity": element[1],
                "name": element[2],
                "price": element[3]
            })
    return cart


def get_user_email(id):
    # Secure Query
    query = "SELECT email FROM users WHERE user_id = ?"
    results = db_query(query, (id))

    
    if len(results) == 0:
        return None
    else:
        return results[0][0]