from handlers.DataBaseCoordinator import db_query

def get_orders(username_orders):

    # Secure Query
    query = "SELECT * FROM %s"
    result = db_query(query, (username_orders,))


    orders = {}

    for element in result:
        current_order_id = element[2]

        if current_order_id not in orders:
            orders[current_order_id] = []
        else:
            orders[current_order_id].append({
                "product_id": element[0],
                "quantity": element[1],
                "name" : get_product_by_id(element[0])["name"],
                "price" : get_product_by_id(element[0])["price"]
            })
    return orders



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
    query = "SELECT * FROM products WHERE product_id = ?"
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
            "review": row[4]
        }
        reviews.append(review)

    return reviews


def check_product_availability(product_id):

    # Secure Query: Check if the ID exists in the specified table
    query = "SELECT available FROM products WHERE product_id = ?;"
    results = db_query(query, (product_id))

    return results[0][0] if results else False


def get_cart(user_id):

    query = "SELECT * FROM carts WHERE user_id=?;"
    result = db_query(query, (user_id))

    cart = []

    for element in result:
        if not ((check_product_availability(element[1]) and verify_product_id_exists(element[1]) and element[2] > 0 and element[2] <= get_product_by_id(element[1])["stock"])):
            delete_query = "DELETE FROM carts WHERE product_id = ? AND user_id = ?;"
            db_query(delete_query, (element[1], user_id))

        else:
            cart.append({
                "product_id": element[1],
                "quantity": element[2],
                "name": get_product_by_id(element[1])["name"],
                "price": get_product_by_id(element[1])["price"]
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