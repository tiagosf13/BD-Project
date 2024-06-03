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



def get_all_products(search_term="", category="", min_price=0, max_price=100000, in_stock=True, sort_order="asc", admin = False):
    in_stock = 1 if in_stock else 0

    if not admin:
        # Secure Query - Select specific columns
        ## TODO podemos fazer isto numa UDF mas mantemos o order by fora
        query = f"""
            SELECT * 
            FROM searchAvailableProducts (?, ?, ?, ?)
            ORDER BY price {sort_order};
        """
        # Add wildcards for LIKE query
        search_term = f"%{search_term}%"
        category = f"%{category}%"
        results = db_query(query, (search_term, category, min_price, max_price))

    else:
        query = f"""
            SELECT * 
            FROM products
            WHERE (product_name LIKE ? OR product_id LIKE ?)
              AND category LIKE ? 
              AND price BETWEEN ? AND ? 
              AND available = ?
            ORDER BY price {sort_order};
        """
        # Add wildcards for LIKE query
        search_term = f"%{search_term}%"
        category = f"%{category}%"
        
        results = db_query(query, (search_term, search_term, category, min_price, max_price, in_stock))
    
    # Execute the query with parameter substitution
    # results = db_query(query, (search_term, category, min_price, max_price, in_stock))
    # Fetch all rows in one go and convert to a list of dictionaries
    products = [{
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "price": row[3],
        "category": row[4],
        "stock": row[5]
    } for row in results]
    
    return products

def verify_product_id_exists(id):
    # Secure Query
    query = "SELECT product_name FROM products WHERE product_id = ?"
    results = db_query(query, (id))

    if len(results) == 0:
        return False
    else:
        return True
    

def get_product_by_id(id: int):
    # Secure Query
    query = "SELECT * FROM getProductById(?)";
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
            "available" : row[6], 
            "average_rating": row[7]
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
            "product_id": row[0],
            "user_id": row[1],
            "review": row[2],
            "rating": row[3],
            "review_date": row[4]
        }
        reviews.append(review)

    return reviews


def check_product_availability(product_id):
    # Secure Query: Check if the ID exists in the specified table
    query = "SELECT available FROM products WHERE product_id = ?;"
    results = db_query(query, (product_id))

    return results[0][0] if results else False


def get_cart(user_id):
    query = "SELECT * FROM getUserCart(?)"
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
    


def get_monthly_sales(year: int = None,
                      month: int = None):
    rows = db_query("SELECT * FROM getMonthlySalesTable(?, ?)", (year, month))

    sales = {}
    for row in rows:
        year = row[0]
        month = row[1]
        total_sales = row[2];
        sales[f"{year}-{month:02d}"] = total_sales;
    return sales