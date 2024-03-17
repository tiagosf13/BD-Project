import re
from handlers.DataBaseCoordinator import db_query, is_valid_table_name


def check_username_exists(username):

    # Execute the query to check if the username exists in the user's table
    # Secure Query
    query = "SELECT CASE WHEN EXISTS (SELECT 1 FROM users WHERE username = ?) THEN 1 ELSE 0 END;"
    result = db_query(query, (username))

    # Return the boolean
    return result[0][0]


def is_valid_input(review_text):
    # Define a regular expression pattern to match valid characters
    valid_characters_pattern = re.compile(r'^[a-zA-Z0-9,.!?()\'" @]+$')

    # Check if the review contains only characters not in the valid pattern
    if not valid_characters_pattern.match(review_text):
        return False

    if re.search(r"<script>", review_text) or re.search(r"onload=", review_text) or re.search(r"<img", review_text):
        return False

    # Check if the review contains a single quote
    if "'" in review_text:
        return False
    
    # If none of the checks above returned False, the review is valid
    return True


def check_email_exists(email):

    #Execute the query to check if the email exists in the user's table
    # Secure Query
    query = "SELECT CASE WHEN EXISTS (SELECT 1 FROM users WHERE email = ?) THEN 1 ELSE 0 END;"
    result = db_query(query, (email))

    # Return the boolean
    return result[0][0]


def check_product_in_cart(user_id, product_id):

    # Secure Query: Check if the product exists in the cart
    query = "SELECT COUNT(*) FROM carts WHERE product_id=? AND user_id=?"
    result = db_query(query, (product_id, user_id))

    # Return the boolean
    return result[0][0]
