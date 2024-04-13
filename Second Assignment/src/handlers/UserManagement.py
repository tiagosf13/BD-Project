import os, random, shutil, secrets, string, requests, hashlib, pandas as pd
from flask import render_template_string
from string import ascii_uppercase, ascii_lowercase
from handlers.EmailHandler import send_email
from handlers.DataBaseCoordinator import db_query
from handlers.ProductManagement import get_product_by_id
from handlers.Verifiers import is_valid_input
from handlers.Retrievers import get_current_dir
from datetime import datetime, timedelta  # For working with token expiration


def clear_reset_token(user_id):
    # Build the query to update the reset_token in the user's table
    # Secure Query
    query = "UPDATE users SET reset_token = NULL WHERE user_id = ?;"
    db_query(query, (user_id))
    query = "UPDATE users SET reset_token_timestamp = NULL WHERE user_id = ?;"
    db_query(query, (user_id))

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
    query = "UPDATE users SET password_reset_token = ? WHERE username = ?"
    db_query(query, (reset_token, user))

    # Secure Query to set the reset_token_timestamp
    query = "UPDATE users SET password_reset_token_timestamp = ? WHERE username = ?"
    db_query(query, (datetime.now(), user))


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




def search_user_by_username(username):

    # Secure Query
    query = "SELECT * FROM users WHERE username = ?"
    result = db_query(query, (username))

    return result[0] if result else None


def search_user_by_email(email):

    # Secure Query
    query = "SELECT * FROM users WHERE email = ?"
    result = db_query(query, (email))

    return result[0][1] if result else None


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
    user = search_user_by_email(email)
    id = get_id_by_username(user)

    # If user is None, return False (user not found)
    if user is None:
        return False
    else:

        # Extract the username and password from the user
        name = user
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
    query_insert = "INSERT INTO users (user_id, username, hashed_password, email, totp_secret_key, totp_secret_key_timestamp, admin_role) OUTPUT INSERTED.user_id VALUES (?, ?, ?, ?, ?, ?, ?);"

    # Execute the insertion query
    id = db_query(query_insert, (id, username, password, email, secret_key, secret_key_timestamp, False))[0][0]

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


def search_user_by_id(id):

    # Construct the SQL query
    # Secure Query
    query = "SELECT * FROM users WHERE user_id = ?"
    result = db_query(query, (id))

    return result[0] if result else None


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

    query = "SELECT * FROM orders WHERE user_id = ?;"
    results = db_query(query, (id))

    # Check if the user has any orders
    if not results:
        return None

    products = []
    product = {}
    for row in results:
        order_id = row[0]
        product_id = row[2]
        order_address = row[5]
        order_date = row[6]

        # Remove milliseconds part from the string
        order_date_str_without_ms = order_date.split('.')[0]

        # Convert the string to a datetime object
        order_date = datetime.strptime(order_date_str_without_ms, "%Y-%m-%d %H:%M:%S")
        
        quantity = row[3]

        # Get product information by id
        product__ = get_product_by_id(product_id)

        product = {
                    "order_id" : order_id,
                    "product_id": product_id,
                    "product_available": product__["available"],
                    "quantity": quantity,
                    "name": product__["name"],
                    "price": product__["price"],
                    "address": order_address,
                    "date": order_date
                }
        products.append(product)

    return products


def get_user_data_by_id(id):

    info = {}
    results = []

    # Construct the SQL query to retrieve the username, email and id
    # Secure Query
    query1 = "SELECT user_id, username, email FROM users WHERE user_id = ?"
    query1_results = db_query(query1, (id))
    results.append(list(query1_results[0]) if query1_results else [])

    # Construct the SQL query to retrieve all the user's orders
    # Secure Query
    query2 = "SELECT * FROM orders WHERE user_id = ?"
    query2_results = db_query(query2, (id))
    results.append(list(query2_results) if query2_results else [])

    # Construct the SQL query to retrieve all the user's reviews
    # Secure Query
    query3 = "SELECT product_id, rating, review_text FROM reviews WHERE user_id = ?"
    query3_results = db_query(query3, (id))
    results.append(list(query3_results) if query3_results else [])

    counter = 0
    for result in results:
        if result:
            if counter == 0:
                info['personal_info'] = [{ "User ID" : result[0], "Username" : result[1], "E-mail" : result[2]}]
            elif counter == 1:
                info['orders'] = [{"Order ID" : order[0], "Product" : get_product_by_id(order[2])["name"], "Product ID" : order[2], "Quantity" : order[3], "Address" : order[5], "Date" : order[6]} for order in result]
            elif counter == 2:
                info['reviews'] = [{"Product ID" : review[0], "Rating" : review[1], "Review" : review[2]} for review in result]
        counter += 1

    # Return the user data
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
