import os, random, shutil, secrets, string, requests, hashlib, pandas as pd
from flask import render_template_string
from string import ascii_uppercase, ascii_lowercase
from handlers.EmailHandler import send_email
from handlers.DataBaseCoordinator import db_query
from handlers.ProductManagement import get_product_by_id
from handlers.Verifiers import is_valid_table_name, is_valid_input
from datetime import datetime, timedelta  # For working with token expiration


def clear_reset_token(user):
    # Build the query to update the reset_token in the user's table
    # Secure Query
    query = "UPDATE users SET reset_token = NULL WHERE username = %s;"
    db_query(query, (user,))
    query = "UPDATE users SET reset_token_timestamp = NULL WHERE username = %s;"
    db_query(query, (user,))

def get_user_by_reset_token(reset_token):

    # Build the query to retrieve the user's data
    # Secure Query
    query = "SELECT * FROM users WHERE reset_token = %s"
    result = db_query(query, (reset_token,))

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
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(code_length))

def generate_emergency_code(code_length=6):
    return ''.join(secrets.choice(string.digits) for i in range(code_length))

# Store the reset token in the user's record in the database
def set_reset_token_for_user(user, reset_token):
    # Store the reset_token in the user's record in the database
    # This may involve creating a new column in the user table to store the token.

    # Build the query to update the reset_token in the user's table

    # Secure Query
    query = "UPDATE users SET reset_token = %s WHERE username = %s"
    db_query(query, (reset_token, user))

    # Secure Query to set the reset_token_timestamp
    query = "UPDATE users SET reset_token_timestamp = %s WHERE username = %s"
    db_query(query, (datetime.now(), user))


# Send a password reset email with the token
def send_password_reset_email(email, reset_token):
    # Use your email library to send a password reset email with a link containing the reset token.
    # The link should point to a password reset route in your application where users can reset their passwords.
    # Make sure the token is securely validated in the reset route.

    # Read the HTML and CSS files
    if os.name == "nt":
        # Get the current working directory
        current_directory = os.path.dirname(os.path.abspath(__file__)).split("\\handlers")[0]
    else:
        # Get the current working directory
        current_directory = os.path.dirname(os.path.abspath(__file__)).split("/handlers")[0]

    with open(current_directory + '/templates/email_password_reset.html', 'r', encoding='utf8') as html_file:
        email_template = html_file.read()

    # Render the email template with the context (including the reset_token)
    body = render_template_string(email_template, reset_token=reset_token)
    
    # Send the recovery email to the user
    return send_email(email, "Reset your password", body)




def search_user_by_username(username):

    # Secure Query
    query = "SELECT * FROM users WHERE username = %s"
    result = db_query(query, (username,))


    # If no user is found, return None
    if not result:
        return None

    # Return the user data
    return result[0]


def search_user_by_email(email):

    # Secure Query
    query = "SELECT * FROM users WHERE email = %s"
    result = db_query(query, (email,))


    # If no user is found, return None
    if not result:

        return None

    # Return the user data
    return result[0][1]


def validate_login(username, password):

    # If username is None, return False (user not found)
    if username is None:
        return False
    else:
        
        # Fetch the user's password
        # Secure Query
        query = "SELECT password FROM users WHERE username = %s"
        result = db_query(query, (username,))


        # Check if there is a password
        if not result:
            return None
        
        # Check if the provided password matches the user's password
        if result[0][0] == password:

            # Return True to indicate the login has been validated
            return True

        else:
            # Return False to indicate the login credentials aren't valid
            return False
        

def get_id_by_username(username):
    # Construct the SQL query
    # Secure Query
    query = "SELECT id FROM users WHERE username = %s"
    result = db_query(query, (username,))


    # Check if 
    if result:
        return str(result[0][0])
    else:
        return None
    

def generate_password(length):

    code = ''

    # Generate a random password
    for i in range(length):
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
    query = "SELECT EXISTS(SELECT 1 FROM users WHERE id = %s);"
    result = db_query(query, (id,))


    return result[0][0]

def check_id_existence_totp_temp(id):
    # Secure Query
    query = "SELECT EXISTS(SELECT 1 FROM totp_temp WHERE id = %s);"
    result = db_query(query, (id,))


    return result[0][0]


def check_order_id_existence(id):
    # Secure Query
    query = "SELECT EXISTS(SELECT 1 FROM all_orders WHERE id = %s);"
    result = db_query(query, (id,))

    return result[0][0]


def generate_random_id():
    # Generate a random ID
    random_id = random.randint(100000, 999999)

    # Check if the generated ID already exists, regenerate if necessary
    while check_id_existence(random_id):
        random_id = random.randint(100000, 999999)

    return random_id

def generate_random_id_totp_temp():
    # Generate a random ID
    random_id = random.randint(100000, 999999)

    # Check if the generated ID already exists, regenerate if necessary
    while check_id_existence_totp_temp(random_id):
        random_id = random.randint(100000, 999999)

    return random_id


def create_user_folder(id):
    try:
        # Get the current working directory
        if os.name == "nt":
            # Get the current working directory
            current_directory = os.path.dirname(os.path.abspath(__file__)).split("\\handlers")[0]
        else:
            # Get the current working directory
            current_directory = os.path.dirname(os.path.abspath(__file__)).split("/handlers")[0]

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
    # Generate a unique user id
    id = str(generate_random_id())

    # Create a folder for the user
    ans = create_user_folder(id)
    
    if ans:
        # Add the user to the USER table
        # Secure Query
        query = "INSERT INTO users (id, username, password, email, secret_key, secret_key_timestamp, admin) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        db_query(query, (id, username, password, email, secret_key, secret_key_timestamp, False))
    
    # Return the created user
    return id, ans


def change_password(id, password):

    # Build the query to update the password in the user's table
    # Secure Query
    query = 'UPDATE users SET password = %s WHERE id = %s'
    db_query(query, (password, id))


def update_username(id, new_username):

    # Get the old username based on the ID
    old_username = search_user_by_id(id)[1]
    
    # Construct the SQL query
    # Secure Query
    query = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s);"
    result = db_query(query, (old_username+"_cart",))


    if result[0][0]:

        # Build the query to alterate the statement username's table
        # Secure Query
        query = "ALTER TABLE "+old_username.lower()+"_cart"+" RENAME TO "+new_username.lower()+"_cart"+";"
        db_query(query)


    query = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s);"
    result = db_query(query, (old_username+"_orders",))
    
    if result[0][0]:

        # Build the query to alterate the statement username's table
        # Secure Query
        query = "ALTER TABLE "+old_username.lower()+"_orders"+" RENAME TO "+new_username.lower()+"_orders"+";"
        db_query(query)


    # Build the query to update the username in the user's table
    # Secure Query
    query = "UPDATE users SET username = %s WHERE id = %s"
    db_query(query, (new_username, id))


def search_user_by_id(id):

    # Construct the SQL query
    # Secure Query
    query = "SELECT * FROM users WHERE id = %s"
    result = db_query(query, (id,))


    # If no user is found, return None
    if not result:
        return None

    # Return the user data
    return result[0]


def update_email(id, email):

    # Verify if the email is valid
    if not is_valid_input(email):
        return False

    # Build the query to update the email in the user's table
    # Secure Query
    query = "UPDATE users SET email = %s WHERE id = %s"
    db_query(query, (email, id))


def update_password(username, password):
    id = str(get_id_by_username(username))
    # Build the query to update the password in the user's table
    # Secure Query
    query = "UPDATE users SET password = %s WHERE id = %s;"
    db_query(query, (str(password), id))


def get_username_by_id(id):
    # Construct the SQL query to retrieve the username
    # Secure Query
    query = "SELECT username FROM users WHERE id = %s;"
    result = db_query(query, (id,))

    # Check if the username was found
    if result:

        # If it was, return the username
        return result[0][0]

    else:

        # If it wasn't return None
        return None
    

def get_user_role(id):

    # Construct the SQL query to retrieve the username
    # Secure Query
    query = "SELECT admin FROM users WHERE id = %s"
    result = db_query(query, (id,))

    # Check if the username was found
    if result:

        # If it was, return the username
        return result[0][0]

    else:

        # If it wasn't return None
        return None


def compose_email_body(products, order_id):
    # Read the HTML and CSS files
    if os.name == "nt":
        # Get the current working directory
        current_directory = os.path.dirname(os.path.abspath(__file__)).split("\\handlers")[0]
    else:
        # Get the current working directory
        current_directory = os.path.dirname(os.path.abspath(__file__)).split("/handlers")[0]

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

    username = get_username_by_id(id).lower()

    # Check if table exists
    # Secure Query
    table_name = username + "_orders"
    if not is_valid_table_name(table_name):
        return None

    query = "SELECT * FROM {};".format(table_name)
    results = db_query(query)

    # Check if the user has any orders
    if not results:
        return None

    products = []
    for row in results:
        order_id = row[0]
        order_address = row[2]
        order_Date = row[4]
        for element in row[1]:
            product__ = get_product_by_id(element)
            if product__ is not None:

                product = {
                    "order_id" : order_id,
                    "product_id": element,
                    "quantity": row[1][element],
                    "name": product__["name"],
                    "price": product__["price"],
                    "address": order_address,
                    "date": order_Date
                }
                products.append(product)

    return products


def get_user_data_by_id(id):

    info = {}
    results = []

    # Construct the SQL query to retrieve the username, email and id
    # Secure Query
    query1 = "SELECT id,username,email FROM users WHERE id = %s"
    query1_results = db_query(query1, (id,))
    results.append(list(query1_results[0]) if query1_results else [])

    # Construct the SQL query to retrieve all the user's orders
    # Secure Query
    query2 = "SELECT id,products,shipping_address,order_date FROM {}_orders".format(results[0][1].lower())
    query2_results = db_query(query2)
    results.append(list(query2_results) if query2_results else [])

    # Construct the SQL query to retrieve all the user's reviews
    # Secure Query
    query3 = "SELECT product_id,rating,review FROM reviews WHERE user_id = %s"
    query3_results = db_query(query3, (id,))
    results.append(list(query3_results) if query3_results else [])

    counter = 0
    for result in results:
        if result:
            if counter == 0:
                info['personal_info'] = [{ "User ID" : result[0], "Username" : result[1], "E-mail" : result[2]}]
            elif counter == 1:
                info['orders'] = [{"Order ID" : order[0], "Product" : get_product_by_id(product)["name"], "Product ID" : product, "Quantity" : order[1][product], "Address" : order[2], "Date" : order[3]} for order in result for product in order[1]]
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

    # Read the HTML and CSS files
    if os.name == "nt":
        # Get the current working directory
        current_directory = os.path.dirname(os.path.abspath(__file__)).split("\\handlers")[0]
    else:
        # Get the current working directory
        current_directory = os.path.dirname(os.path.abspath(__file__)).split("/handlers")[0]

    print(current_directory)

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
