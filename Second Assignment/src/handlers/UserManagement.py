from http.client import PRECONDITION_FAILED
import os, random, shutil, secrets, string, requests, hashlib, pandas as pd
from flask import render_template_string
from string import ascii_uppercase, ascii_lowercase
from handlers.EmailHandler import send_email
from handlers.DataBaseCoordinator import db_query
from handlers.ProductManagement import get_product_by_id
from handlers.Verifiers import is_valid_input
from handlers.Retrievers import get_current_dir
from datetime import datetime, timedelta  # For working with token expiration


def search_user(search_regex, search_regex_value, select_attribute = "*"):

    # Search user by a given regex
    query = f"SELECT {select_attribute} FROM users WHERE {search_regex} = ?;"
    result = db_query(query, (search_regex_value))
    attributes_lst = [
        "user_id",
        "username",
        "hashed_password",
        "password_reset_token",
        "password_reset_token_timestamp",
        "email",
        "totp_secret_key",
        "totp_secret_key_timestamp",
        "admin_role"
    ]

    select_attribute_split = select_attribute.split(",") if select_attribute != "*" else attributes_lst


    # Create a dictionary to store the user's information
    dic = {}
    if result:
        for i in range(len(result[0])):
            dic[select_attribute_split[i].strip()] = result[0][i]
        return dic
    else:
        return None



def clear_reset_token(user_id):
    # Build the query to update the reset_token in the user's table
    # Secure Query
    query = """
        UPDATE users SET reset_token = NULL WHERE user_id = ?;
        UPDATE users SET reset_token_timestamp = NULL WHERE user_id = ?;
    """
    db_query(query, (user_id, user_id))

def get_user_by_reset_token(reset_token):

    # Build the query to retrieve the user's data
    # Secure Query
    query = "SELECT user_id FROM users WHERE password_reset_token = ?"
    result = db_query(query, (reset_token))

    return result[0] if result else None

# This function checks if the reset token is valid and not expired.
def is_valid_reset_token(reset_token):
    user = get_user_by_reset_token(reset_token)
    
    if user:
        # Assuming 'reset_token_timestamp' is a field in your User model to store the token creation timestamp.
        token_timestamp = user[4]

        # Define the token expiration time (10 minutes).
        token_expiration_time = timedelta(minutes=10)

        # Check if the token is not expired.
        if token_timestamp + token_expiration_time >= datetime.now():
            return True
    return False


# Generate a unique reset token
def generate_reset_token(code_length=32):
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(code_length))

def generate_emergency_code(code_length=6):
    return ''.join(secrets.choice(string.digits) for i in range(code_length))

# Store the reset token in the user's record in the database
def set_reset_token_for_user(user, reset_token):
    # Store the reset_token in the user's record in the database
    # This may involve creating a new column in the user table to store the token.

    # Build the query to update the reset_token in the user's table

    # Secure Query
    query = """
        UPDATE users SET password_reset_token = ? WHERE username = ?;
        UPDATE users SET password_reset_token_timestamp = ? WHERE username = ?
    """
    db_query(query, (reset_token, user, datetime.now(), user))


# Send a password reset email with the token
def send_password_reset_email(email, reset_token):
    # Use your email library to send a password reset email with a link containing the reset token.
    # The link should point to a password reset route in your application where users can reset their passwords.
    # Make sure the token is securely validated in the reset route.

    with open(get_current_dir() + '/templates/email_password_reset.html', 'r', encoding='utf8') as html_file:
        email_template = html_file.read()

    # Render the email template with the context (including the reset_token)
    body = render_template_string(email_template, reset_token=reset_token)
    
    # Send the recovery email to the user
    return send_email(email, "Reset your password", body)


def validate_login(username, password):

    # If username is None, return False (user not found)
    if username is None:
        return False
    else:
        
        # Fetch the user's password
        # Secure Query
        query = "SELECT password FROM users WHERE username = ?"
        result = db_query(query, (username))

        return result[0][0] == password if result else None

def get_id_by_username(username):
    # Construct the SQL query
    # Secure Query
    query = "SELECT user_id FROM users WHERE username = ?"
    result = db_query(query, (username))
    
    return str(result[0][0]) if result else None

def generate_password(length):

    code = ''
    # Generate a random password
    for _ in range(length):
        code += random.choice(ascii_uppercase + ascii_lowercase + '0123456789')

    return code

def send_recovery_password(email):

    # Search for the user with the given email
    user = search_user(email, "email")
    id = get_id_by_username(user)

    # If user is None, return False (user not found)
    if user is None:
        return False
    else:

        # Extract the username and password from the user
        name = user["username"]
        password = generate_password(15)
        change_password(id, password)

        # Build the HTML body
        HTMLBody = f"""
            <html>
            <head>
                <style>
                body {{
                    font-family: Arial, sans-serif;
                    font-size: 14px;
                    color: #333;
                }}
                h1 {{
                    color: #007bff;
                }}
                p {{
                    margin-bottom: 10px;
                }}
                </style>
            </head>
            <body>
                <h1>Recover Password</h1>
                <p>Hello, {name}</p>
                <p>Your new password is: <strong>{password}</strong></p>
            </body>
            </html>
        """

        # Send the recovery email to the user
        send_email(email, "Recover your password", HTMLBody)

        # Return True to indicate the email was sent successfully
        return True
    

def check_id_existence(id):
    # Secure Query
    query = "IF EXISTS(SELECT 1 FROM users WHERE user_id = ?) SELECT 1 ELSE SELECT 0;"
    result = db_query(query, (id))

    return result[0][0]


def check_order_id_existence(id):
    # Secure Query
    query = "IF EXISTS(SELECT 1 FROM all_orders WHERE id = ?) SELECT 1 ELSE SELECT 0;"
    result = db_query(query, (id))

    return result[0][0]


def generate_random_id():
    # Generate a random ID
    random_id = random.randint(100000, 999999)

    # Check if the generated ID already exists, regenerate if necessary
    while check_id_existence(random_id):
        random_id = random.randint(100000, 999999)

    return random_id


def create_user_folder(id):
    try:
        # Get the current working directory
        current_directory = get_current_dir()

        # Define the path for the user's directory
        user_directory = os.path.join(current_directory, "database", "accounts")

        # Set the paths for the source and destination files
        src_path = os.path.join(current_directory, "static", "images", "default.png")
        dst_path = os.path.join(user_directory, f"{id}.png")

        # Check if the user directory exists, create if it doesn't
        if not os.path.exists(user_directory):
            os.makedirs(user_directory)

        # Copy the source file to the destination file
        shutil.copy(src_path, dst_path)
        return True
    except:
        return False


def create_user(username, password, email, secret_key, secret_key_timestamp):

    id = generate_random_id()

    # Secure Query
    # Assuming you are using SQL Server
    query_insert = "INSERT INTO users (user_id, username, hashed_password, email, totp_secret_key, totp_secret_key_timestamp, admin_role) VALUES (?, ?, ?, ?, ?, ?, ?);"

    # Execute the insertion query
    db_query(query_insert, (id, username, password, email, secret_key, secret_key_timestamp, False))

    # Create a folder for the user
    ans = create_user_folder(id)

    # Return the created user
    return id, ans



def change_password(id, password):

    # Build the query to update the password in the user's table
    # Secure Query
    query = 'UPDATE users SET password = ? WHERE id = ?'
    db_query(query, (password, id))


def update_username(id, new_username):

    # Build the query to update the username in the user's table
    # Secure Query
    query = "UPDATE users SET username = ? WHERE user_id = ?"
    db_query(query, (new_username, id))


def update_email(id, email):

    # Verify if the email is valid
    if not is_valid_input(email):
        return False

    # Build the query to update the email in the user's table
    # Secure Query
    query = "UPDATE users SET email = ? WHERE user_id = ?"
    db_query(query, (email, id))


def update_password(username, password):
    id = str(get_id_by_username(username))
    # Build the query to update the password in the user's table
    # Secure Query
    query = "UPDATE users SET hashed_password = ? WHERE user_id = ?;"
    db_query(query, (str(password), id))


def get_username_by_id(id):
    # Construct the SQL query to retrieve the username
    # Secure Query
    query = "SELECT username FROM users WHERE user_id = ?;"
    result = db_query(query, (id))

    return result[0][0] if result else None

def get_user_role(id):

    if not id:
        return False

    # Construct the SQL query to retrieve the username
    # Secure Query
    query = "SELECT admin_role FROM users WHERE user_id = ?;"
    result = db_query(query, (id))

    # Check if the username was found
    return result[0][0] if result else None

def compose_email_body(products, order_id):
    
    current_directory = get_current_dir()

    with open(current_directory + '/templates/email_order.html', 'r', encoding='utf8') as html_file:
        email_template = html_file.read()

    with open(current_directory + '/static/css/email_order.css', 'r', encoding='utf8') as css_file:
        css_styles = css_file.read()

    # Create a context dictionary with the products and total_price
    context = {
        'products': products,
        'total_price': calculate_total_price(products),  # Calculate the total price here]
        'order_id': order_id
    }

    # Render the email template with the context
    body = render_template_string(email_template, **context)
    body = body.replace('{{ css_styles }}', css_styles)

    return body

def calculate_total_price(products):
    total_price = 0
    for product in products:
        total_price += int(product['quantity']) * float(product['price'])
    return total_price


def get_orders_by_user_id(id):

    # query = "SELECT orders.order_id, product_id, shipping_address, order_date, quantity FROM orders \
    #         LEFT JOIN products_ordered ON orders.order_id = products_ordered.order_id \
    #         WHERE orders.user_id = ?;"
    query = "SELECT * from getUserOrders(?)"
    results = db_query(query, (id))

    # Check if the user has any orders
    if not results:
        return None

    orders = {}
    for row in results:
        order_id = row[0]
        order_date = row[1]
        product_id = row[2]
        product_name = row[3]
        category = row[4]
        price = row[5]
        quantity = row[6]
        total_price = row[7]
        available = row[8]
        reviewed = row[9]

        product = {
                    "order_date": order_date,
                    "product_id": product_id,
                    "name": product_name,
                    "category": category,
                    "quantity": quantity,
                    "price": price,
                    "total_price": total_price,
                    "product_available": available,
                    "reviewed" : reviewed
                }
        products = orders.get(order_id, [])
        products.append(product)
        orders[order_id] = products

    return orders


def check_user_bought_product(user_id, product_id):
    # Construct the SQL query to check if the user bought the product
    # Secure Query
    query = """
        SELECT products_ordered.order_id 
        FROM products_ordered 
            JOIN orders ON products_ordered.order_id = orders.order_id
        WHERE orders.user_id = ? AND products_ordered.product_id = ?;
    """
    result = db_query(query, (user_id, product_id))

    return True if result else False


def get_user_data_by_id(id):
    info = {}
    print("User ID: ", id)
    # Construct the SQL query to retrieve user's info, orders, and reviews
    ## Transformado numa view
    query = """
        SELECT *
        FROM CompleteUserData
        WHERE user_id = ?;
    """
    query_results = db_query(query, (id,))
    print(query_results)

    if query_results:
        for row in query_results:
            if 'personal_info' not in info:
                info['personal_info'] = [{"User ID": row[0], "Username": row[1], "E-mail": row[2]}]
            if 'orders' not in info and row[3] != None:
                info['orders'] = [{"Order ID": row[3], "Product": get_product_by_id(row[4])["name"], "Product ID": row[4], "Quantity": row[5], "Address": row[6], "Date": row[7]}]
            if 'reviews' not in info and row[4] != None:
                info['reviews'] = [{"Product ID": row[4], "Rating": row[8], "Review": row[9]}]
    else:
        info = {}
        
    print("Info:", info)

    return info


def check_password(password):
    # Hash the password using SHA-1
    hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = hashed_password[:5], hashed_password[5:]

    # Make a GET request to the HIBP API
    response = requests.get(f'https://api.pwnedpasswords.com/range/{prefix}')

    # Check if the suffix of the hashed password exists in the response
    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return int(count)
    return 0


def generate_excel_user_data(id):

    data = get_user_data_by_id(id)

    # Convert data to DataFrame if the keys exist
    df_personal_info = pd.DataFrame(data.get('personal_info', []))
    df_reviews = pd.DataFrame(data.get('reviews', []))
    df_orders = pd.DataFrame(data.get('orders', []))

    current_directory = get_current_dir()

    # Check if the directory exists
    user_data_directory = os.path.join(current_directory, "database", "user_data")
    if not os.path.exists(user_data_directory):
        os.makedirs(user_data_directory)

    # Create an Excel writer using pandas with openpyxl engine
    with pd.ExcelWriter(os.path.join(user_data_directory, f"{id}.xlsx"), engine='openpyxl') as writer:
        # Write each DataFrame to a separate sheet in the Excel file if they exist
        if not df_personal_info.empty:
            df_personal_info.to_excel(writer, sheet_name='Personal Info', index=False)
        if not df_reviews.empty:
            df_reviews.to_excel(writer, sheet_name='Reviews', index=False)
        if not df_orders.empty:
            df_orders.to_excel(writer, sheet_name='Orders', index=False)
    
    return current_directory
