import os, tempfile
from handlers.extensions import bcrypt
from handlers.UserManagement import search_user_by_email, get_id_by_username, send_password_reset_email
from flask import Blueprint, request, session, render_template, jsonify, redirect, url_for, send_from_directory, send_file
from handlers.UserManagement import search_user_by_username, create_user, get_orders_by_user_id, generate_random_id_totp_temp, check_password, generate_excel_user_data
from handlers.UserManagement import update_username, search_user_by_id, update_email, is_valid_reset_token, get_user_by_reset_token, clear_reset_token
from handlers.UserManagement import get_user_role, compose_email_body, update_password, generate_reset_token, set_reset_token_for_user
from handlers.ProductManagement import create_review, set_cart_item, update_product_after_order, register_order
from handlers.ProductManagement import create_product, remove_product, verify_id_exists, update_product_name, create_product_image
from handlers.ProductManagement import update_product_description, update_product_price, update_product_category, update_product_quantity
from handlers.EmailHandler import send_email_with_attachment, sql_to_pdf
from handlers.DataBaseCoordinator import check_database_table_exists, db_query, is_valid_table_name
from handlers.Verifiers import check_username_exists, check_email_exists, check_product_in_cart, is_valid_input
from handlers.Retrievers import get_all_products, get_product_by_id, get_product_reviews, get_cart, get_user_email
from handlers.TOTPHandler import  remove_valid_emergency_code, get_user_emergency_codes, get_totp_secret, generate_qr_code
from handlers.TOTPHandler import generate_totp_atributes, verify_totp_code, store_totp_stage, get_totp_atributes, generate_emergency_codes



# Starting Blueprint
views = Blueprint('views', __name__)


# Check if the database tables exist
check_database_table_exists("users")
check_database_table_exists("products")
check_database_table_exists("reviews")
check_database_table_exists("all_orders")
check_database_table_exists("totp_temp")
check_database_table_exists("emergency_codes")


# This route is used to serve the index page
@views.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# This route is used to perform the login
@views.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")

        if is_valid_input(username) == False:
            return render_template("login.html", message="Invalid username.")

        user = search_user_by_username(username)
        id = get_id_by_username(username)

        if user and bcrypt.check_password_hash(user[2], password):
            return redirect(url_for("views.verify_totp_login", id=id))

        # Password is incorrect
        return render_template("login.html", message="Invalid login credentials.")
    
    else:
        return render_template("login.html")


@views.route('/logout', methods=['GET'])
def logout():

    # Clear the session variables
    session.clear()

    # Return the login page
    return redirect(url_for("views.login"))


# This view is used to enroll new users into the platform
@views.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")
        email = request.form.get("email")

        if is_valid_input(username) == False or is_valid_input(email) == False:
            return render_template("signup.html", message="Invalid username.")


        # Check if there is no user in the database using the same email or the same username
        if search_user_by_email(email) != None or search_user_by_username(username) != None:
            return render_template("signup.html", message="User already exists.")
        else:
            # Hash the password before storing it in the database
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

            session["signup_hashed_password"] = hashed_password
            session["signup_username"] = username
            session["signup_email"] = email

            return render_template("information_collected.html")
    else:
        return render_template("signup.html")


@views.route('/validate_consent', methods=['POST'])
def validate_consent():
    consent = request.form.get('consent')
    if consent:
        temp_id = str(generate_random_id_totp_temp())

        username = session.get("signup_username")
        email = session.get("signup_email")
        hashed_password = session.get("signup_hashed_password")

        secret_key, secret_key_timestamp, qr_code_base64 = generate_totp_atributes(username)

        store_totp_stage(temp_id, username, secret_key, secret_key_timestamp, email, hashed_password)

        # Clean the session variables
        session.pop("signup_username", None)
        session.pop("signup_email", None)
        session.pop("signup_hashed_password", None)

        return render_template('totp_signup.html', secret_key=secret_key, qr_code=qr_code_base64, id=temp_id)
    else:
        return redirect(url_for("views.signup"))


@views.route('verify_totp_signup/<id>', methods=['POST'])
def verify_totp_signup(id):

    token = request.form.get("token")

    if token == None:
        return render_template("signup.html", message="Invalid TOTP code. Please try again.")

    # Verify the TOTP code
    if verify_totp_code(id, token, 'totp_temp'):

        # Get all the atributes from the temporary table
        username, email, hashed_password, secret_key, secret_key_timestamp = get_totp_atributes(id)

        # Create the user in the database with the hashed password
        id, ans = create_user(username, hashed_password, email, secret_key, secret_key_timestamp)

        # Clear the temporary table
        query = "DELETE FROM totp_temp WHERE id = %s"
        db_query(query, (id,))

        if ans == False:
            return render_template("signup.html", message="Error! Please try again.")
        else:
            # Redirect to the emergency codes page
            return redirect(url_for("views.emergency_codes", id=id))
    else:
        return render_template("signup.html", message="Invalid TOTP code. Please try again.")
    
@views.route('/totp_profile/<id>', methods=['GET'])
def totp_profile(id):

    if id == None:
        return redirect(url_for("views.login"))

    username = search_user_by_id(id)[1]

    if username == None:
        return redirect(url_for("views.login"))
    
    secret_key = get_totp_secret(id)

    qr_code_base64 = generate_qr_code(secret_key, username)

    return render_template("totp_profile.html", id=id, secret_key=secret_key, qr_code=qr_code_base64, username=username)


@views.route('/new_emergency_codes/<id>', methods=['GET'])
def new_emergency_codes(id):

    if id == None:
        return redirect(url_for("views.login"))

    username = search_user_by_id(id)[1]

    if username == None:
        return redirect(url_for("views.login"))
    
    generate_emergency_codes(id, reset=True)

    return render_template("new_emergency_codes.html", id=id, username=username)


@views.route('/emergency_codes/<id>', methods=['GET'])
def emergency_codes(id):

    if id == None:
        return redirect(url_for("views.login"))

    username = search_user_by_id(id)[1]

    if username == None:
        return redirect(url_for("views.login"))

    return render_template("emergency_codes.html", id=id)

@views.route('/get_codes/<id>', methods=['GET'])
def get_emergency_codes(id):

    # Generate 10 emergency codes, each with 15 characters (Upper case letters, Lower case letters, Special characters and numbers)
    codes = generate_emergency_codes(id)

    # Logic to fetch codes (replace with your actual data retrieval)
    return jsonify({'codes': codes})


@views.route('/verify_totp_login/<id>', methods=['POST', 'GET'])
def verify_totp_login(id):

    if id == None:
        return redirect(url_for("views.login"))

    if request.method == "GET":
        return render_template("totp_login.html", id=id)
    else:
        username = search_user_by_id(id)[1]
        token = request.get_json().get("token") if request.is_json else None
        
        if username is None or token is None:
            return render_template("login.html", message="Invalid TOTP code. Please try again.")
        
        verified = verify_totp_code(id, token, 'users', username=username)

        # Verify the TOTP code
        if verified == True:
            # Set session variables
            session["username"] = username
            session["id"] = id
            session["admin"] = get_user_role(session["id"])

            # Check for table existence
            check_database_table_exists(username.lower() + "_cart")
            check_database_table_exists(f"{username.lower()}_orders")

            return jsonify({'message': 'Login successful.'}), 200
        else:

            # Get all the emergency codes
            emergency_codes = get_user_emergency_codes(id)

            # Check if the token is an emergency code
            if token!=None and token in emergency_codes and emergency_codes[token] == True:
                remove_valid_emergency_code(id, token)
                # Set session variables
                session["username"] = username
                session["id"] = id
                session["admin"] = get_user_role(session["id"])
                return jsonify({'message': 'Login successful.'}), 200

            # Return a JSON response indicating failure with status code 500
            return jsonify({'error': 'Invalid TOTP code. Please try again.'}), 500

# This route is used to let the user reset their password
@views.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        email = request.form.get("email")
        if is_valid_input(email) == False:
            return render_template("reset-password.html", message="Invalid email.")

        user = search_user_by_email(email)
        if user is None:
            # If the user doesn't exist, return the signup page
            return redirect(url_for("views.signup"))
        else:
            # Generate a unique reset token
            reset_token = generate_reset_token()
            # Store the reset token in the user's record in the database
            set_reset_token_for_user(user, reset_token)
            # Send a password reset email with the token
            send_password_reset_email(email, reset_token)
            return redirect(url_for("views.login"))
    else:
        return render_template("reset-password.html")


@views.route('/reset_password/<reset_token>', methods=['GET', 'POST'])
def reset_password_confirm(reset_token):
    # Check if the reset token is valid and not expired
    if is_valid_reset_token(reset_token):
        if request.method == 'POST':
            new_password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            if new_password == confirm_password:
                # Update the user's password in the database with the new hashed password
                username = get_user_by_reset_token(reset_token)[1]

                if username:
                    hashed_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
                    update_password(username, hashed_password)

                    # Clear the reset token for security
                    clear_reset_token(username)
                    return redirect(url_for('views.login'))
        return render_template('reset_password.html', reset_token=reset_token)
    else:
        clear_reset_token(username)
        return redirect(url_for('views.login'))



# This view returns the account settings page
@views.route("/profile/<username>", methods=['GET'])
def profile(username):
    
    if is_valid_input(username) == False:
        return render_template("index.html", message="Invalid username.")

    # Get ID based on the username
    id = session.get("id")

    if id == None:
        return redirect(url_for("views.login"))

    # Return the account settings page 
    return render_template("profile.html", username=username, id=id)


# This view is used to check if te username exits
@views.route('/check_username', methods=['POST'])
def check_username():

    # Get the username from the request
    username = request.form.get('username')

    if is_valid_input(username) == False:
        return render_template("signup.html", message="Invalid username.")

    # Check if the username exists
    exists = check_username_exists(username)

    # Build response dictionary with the boolean
    response = {'exists': exists}

    # Return the response as a JSON object
    return jsonify(response)


# This view is used to check if te email exits
@views.route('/check_email', methods=['POST'])
def check_email():

    # Get the email from the request
    email = request.form.get('email')

    if is_valid_input(email) == False:
        return render_template("signup.html", message="Invalid email.")

    # Check if the username exists
    exists = check_email_exists(email)

    # Build response dictionary with the boolean
    response = {'exists': exists}

    # Return the response as a JSON object
    return jsonify(response)


@views.route('/update_account/<id>', methods=['POST'])
def update_account(id):

    if id == None and session.get("id") == None:
        return redirect(url_for("views.login"))
    
    try:
    
        if os.name == "nt":
            # Get the current working directory
            current_directory = os.path.dirname(os.path.abspath(__file__)).split("\\handlers")[0]
        else:
            # Get the current working directory
            current_directory = os.path.dirname(os.path.abspath(__file__)).split("/handlers")[0]
            
        accounts_directory = os.path.join(current_directory, "database", "accounts")
        os.makedirs(accounts_directory, exist_ok=True)  # Ensure the directory exists

        file_path = os.path.join(accounts_directory, f"{id}.png").replace("\\", "/")

        # Get the new uploaded user's account image
        profile_photo = request.files.get("profile_photo")

        # If there is an image and the size is less than 5MB
        if profile_photo and not profile_photo.content_length > 5120 * 5120:
            # Save the image to the user's account
            profile_photo.save(file_path)

        # Get the username, email, and password from the user's session
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("psw")
        old_password = request.form.get("psw-old")

        # Check if the username field wasn't empty and occupied by another user
        if username != "" and not check_username_exists(username) and is_valid_input(username):

            # Update the username
            update_username(id, username)

            # Set the session's username
            session["username"] = username

        else:
            # If there is a problem with the username, get the username based on the ID
            username = search_user_by_id(id)[1]

        # Check if the email field wasn't empty and occupied by another user
        if email != "" and not check_email_exists(email) and is_valid_input(email):

            # Update the email
            update_email(id, email)

        else:
            # If there is a problem with the email, get the email based on the ID
            email = search_user_by_id(id)[3]

        # Check if the password wasn't empty
        if password != "":
            # Update the password
            # Hash the password before storing it in the database

            if bcrypt.check_password_hash(search_user_by_id(id)[2], old_password):
                hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
                username = search_user_by_id(id)[1]
                update_password(username, hashed_password)
            else:
                return render_template("profile.html", message="Invalid password.", username=username, id=id)

        # Return the profile page
        return redirect(url_for("views.catalog", id=id))
    
    except Exception as e:
        print(e)
        return render_template("profile.html", message="Invalid input.", username=username, id=id)


# This view is used to get a image
@views.route('/get_image/<path:filename>', methods=['GET'])
def get_image(filename):

    if 'database' in filename and session.get("id") is None:
        return redirect(url_for("views.login"))

    # Send the image
    path = "/".join(filename.split("/")[:-1])
    filename = filename.split("/")[-1]
    return send_from_directory(path, filename)


@views.route('/catalog/<id>', methods=['GET'])
def catalog(id):
    if id == None or session.get("id") == None:
        return redirect(url_for("views.login"))

    # Get the username and id from the session
    name = search_user_by_id(id)[1]
    admin = get_user_role(id)

    if is_valid_input(name) == False:
        return render_template("index.html", message="Invalid username.")

    if admin:
        return render_template("catalog_admin.html", username=name, id=id, admin=admin)
    else:
        # Return the catalog page
        return render_template("catalog.html", username=name, id=id, admin=admin)


@views.route('/products', methods=['GET'])
def products():

    products = get_all_products()

    return jsonify(products)


@views.route('/add_product/<id>', methods=['POST'])
def add_product(id):

    if id == None:
        return redirect(url_for("views.login"))

    if id is not None and is_valid_input(id) is not False:
    
        product_name = request.form.get("productName")
        product_description = request.form.get("productDescription")
        product_price = request.form.get("productPrice")
        product_category = request.form.get("productCategory")
        product_quantity = request.form.get("productUnits")
        product_photo = request.files.get("productImage")

        preconditions = is_valid_input(product_name) == False or \
                        is_valid_input(product_description) == False or \
                        is_valid_input(product_price) == False or \
                        is_valid_input(product_category) == False or \
                        is_valid_input(product_quantity) == False or \
                        product_photo and product_photo.content_length > 5120 * 5120 # Verify that the size of the image is less than 5MB

        if preconditions:
            return redirect(url_for("views.catalog", id=id))
        else:
            create_product(product_name, product_description, product_price, product_category, product_quantity, product_photo)

    return redirect(url_for("views.catalog", id=id))


@views.route('/remove_product/<id>', methods=['POST'])
def remove_product_by_id(id):
    # Updated route name and parameter name to avoid conflicts
    product_id = request.form.get("productId")

    if is_valid_input(product_id) != False and id is not None and verify_id_exists(product_id, "products"):
        # Assuming 'remove_product' is a function you've defined elsewhere, you can use it here
        remove_product(product_id)

    return redirect(url_for("views.catalog", id=id))


@views.route('/edit_product/<id>', methods=['POST'])
def edit_product_by_id(id):

    product_id = request.form.get("productId")
    product_name = request.form.get("productName")
    product_description = request.form.get("productDescription")
    product_price = request.form.get("productPrice")
    product_category = request.form.get("productCategory")
    product_quantity = request.form.get("productUnits")
    product_photo = request.files.get("productImage")

    if id is None:
        return redirect(url_for("views.login"))

    if is_valid_input(product_id) and verify_id_exists(product_id, "products"):
        if product_name != "" and is_valid_input(product_name):
            update_product_name(product_id, product_name)
        if product_description != "" and is_valid_input(product_description):
            update_product_description(product_id, product_description)
        if product_price != "" and is_valid_input(product_price):
            update_product_price(product_id, product_price)
        if product_category != "" and is_valid_input(product_category):
            update_product_category(product_id, product_category)
        if product_quantity != "" and is_valid_input(product_quantity):
            update_product_quantity(product_id, product_quantity)
        if product_photo:
            create_product_image(product_id, product_photo)


    return redirect(url_for("views.catalog", id=id))


@views.route('/product-quantities/<id>', methods=['GET'])
def product_quantities(id):

    if id is None:
        return redirect(url_for("views.login"))

    products = get_all_products()

    return render_template('product_quantities.html', products=products)


@views.route('/product/<int:product_id>/', methods=['GET'])
def product_page(product_id):
    # Fetch the product details based on the product_id
    # You can retrieve the product information from your data source
    id = session.get("id")
    product = get_product_by_id(product_id)
    admin = get_user_role(id)

    if verify_id_exists(product_id, "products") == False:
        return redirect(url_for("views.catalog", id=id))
    elif id == None:
        # Pass the product details to the template
        return render_template('product_anonymous.html', product = product)
    elif admin:
        return render_template('product_admin.html', product = product)
    else:
        # Pass the product details to the template
        return render_template('product.html', product = product)


@views.route('/get_reviews/<int:product_id>/', methods=['GET'])
def get_reviews(product_id):

    reviews = get_product_reviews(product_id)

    if reviews == None:
        return jsonify([])
    else:
        for element in reviews:
            element["username"] = search_user_by_id(element["user_id"])[1]

    return jsonify(reviews)


@views.route('/add_review/<product_id>/', methods=['POST'])
def add_review(product_id):

    # Get the user's id and username from the session
    user_id = session.get("id")
    username = search_user_by_id(user_id)[1]

    if user_id == None:
        return redirect(url_for("views.login"))

    # Get the review and rating from the request
    review = request.form.get("userReview")
    rating = request.form.get("rating")

    if not is_valid_input(review) or verify_id_exists(product_id, "products") == False or rating == None:
        return jsonify({'error': 'Invalid review.'}), 500
    

    # Create the review
    create_review(product_id, user_id, review, rating)

    # Return a JSON response with the correct content type
    response_data = {'message': 'Review added successfully', "username": username}
    return jsonify(response_data), 200, {'Content-Type': 'application/json'}


@views.route('/add_item_cart/<int:product_id>', methods=['POST'])
def add_item_to_cart(product_id):

    id = session.get("id")
    if id == None:
        return redirect(url_for("views.login"))
    elif verify_id_exists(product_id, "products") == False:
        return redirect(url_for("views.catalog", id=id))
    
    username = search_user_by_id(id)[1].lower()
    try:
        data = request.get_json()
        quantity = data.get('quantity')

        if quantity <= 0:
            return jsonify({'error': 'Invalid quantity.'}), 500
        
        if not is_valid_table_name(username + "_cart"):
            return jsonify({'error': 'Invalid table name.'}), 400
        
        # Secure Query
        query = "SELECT * FROM {} WHERE product_id = %s".format(username + "_cart")
        result = db_query(query, (product_id,))

        product_stock = get_product_by_id(product_id)["stock"]

        if result != [] and result[0][1] + quantity > product_stock:
            return jsonify({'error': 'Not enough stock.'}), 500
        elif result == [] and (quantity > product_stock):
            return jsonify({'error': 'Not enough stock.'}), 500
        else:
            set_cart_item(username + "_cart", product_id, quantity, "add")
            return jsonify({'message': 'Product added to the cart.'}), 200
        
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    


@views.route('/remove_item_cart/<int:product_id>', methods=['POST'])
def remove_item_from_cart(product_id):

    id = session.get("id")

    if id == None:
        return redirect(url_for("views.login"))
    
    elif verify_id_exists(product_id, "products") == False:
        return redirect(url_for("views.catalog", id=id))

    username = search_user_by_id(id)[1].lower()
    try:
        data = request.get_json()
        quantity = data.get('quantity')

        # Secure Query: Validate the table name
        cart_table_name = f"{username}_cart"

        if not is_valid_table_name(cart_table_name):
            return jsonify({'error': 'Invalid table name.'}), 400

        if check_product_in_cart(cart_table_name, product_id) == False or quantity <= 0:
            return jsonify({'error': 'Product not in cart.'}), 500
        else:
            # Secure Query
            query = "SELECT * FROM {} WHERE product_id = %s".format(cart_table_name)
            result = db_query(query, (product_id,))

            if result != [] and result[0][1] == quantity:
                # Remove the product from the cart
                # Secure Query
                query = "DELETE FROM {} WHERE product_id = %s".format(cart_table_name)
                db_query(query, (product_id,))
                return jsonify({'message': 'Product removed from the cart.'}), 200
            elif result != [] and result[0][1] - quantity >= 0:
                # Secure Query: Update the user's cart in the database
                set_cart_item(cart_table_name, product_id, quantity, "remove")
                return jsonify({'message': 'Product removed from the cart.'}), 200
            else:
                return jsonify({'message': 'Product not in the cart.'}), 500
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


@views.route('/get_cart_items/', methods=['GET'])
def get_cart_items():
    id = session.get("id")
    if id == None:
        return redirect(url_for("views.login"))
    
    user_cart = get_cart(search_user_by_id(id)[1].lower() + "_cart")

    return jsonify(user_cart)



@views.route('/remove_all_items_cart/', methods=['POST'])
def remove_all_items_cart():

    id = session.get("id")
    if id == None:
        return redirect(url_for("views.login"))

    username = search_user_by_id(id)[1].lower()

    # Remove all the products from the cart
    # Secure Query: Validate the table name
    table_name = username + "_cart"
    if not is_valid_table_name(table_name):
        return jsonify({'error': 'Invalid table name.'}), 400

    # Remove all the products from the cart
    # Secure Query
    query = "DELETE FROM {}".format(table_name)
    db_query(query)

    return jsonify({'message': 'Cart cleared.'}), 200


@views.route('/checkout', methods=['POST', 'GET'])
def checkout():

    user_id = session.get("id")

    if user_id == None:
        return redirect(url_for("views.login"))

    username = search_user_by_id(user_id)[1].lower()
    if request.method == 'POST':
        # Get form data from the request
        data = request.get_json()
        # get the products from the cart
        products = get_cart(username + "_cart")

        for element in products:
            element["price"] = float(element["price"])
            element["quantity"] = int(element["quantity"])

        # Create an order object (you can customize this based on your needs)
        order_details = {
            'first_name': data['firstName'],
            'last_name': data['lastName'],
            'shipping_address': data['address'],
            'credit_card': data['creditCard'],
            'expiration_date': data['expirationDate'],
            'cvv': data['cvv']
        }

        # Add the order to the database
        response, order_id = register_order(username, user_id, order_details, products)

        if response:
            update_product_after_order(products)
            body = compose_email_body(products, order_id)
            to = get_user_email(user_id)

            # Create a temporary directory to store the PDF
            with tempfile.TemporaryDirectory() as temp_dir:
                pdf_path = os.path.join(temp_dir, f'order_{order_id}.pdf')
                sql_to_pdf(username, pdf_path)
                
                # Send the order confirmation email with the PDF attachment
                send_email_with_attachment(to, 'Order Confirmation', body, pdf_path)

            # Clear the cart
            # Secure Query: Validate the table name
            cart_table_name = f"{username}_cart"
            if not is_valid_table_name(cart_table_name):
                return jsonify({'error': 'Invalid table name.'}), 400

            query = "DELETE FROM {}".format(cart_table_name)
            db_query(query, ())


            # Redirect to a thank you page or any other appropriate page
            return jsonify({'message': 'Order placed successfully.'}), 200
        else:
            return jsonify({'error': 'Something went wrong.'}), 500
    else:
        # Handle GET request (display the checkout page), use .json to convert the response to JSON (otherwise we get the 200 OK response)
        products = get_cart_items().json

        if not products:
            return redirect(url_for('views.catalog', id=user_id))
        return render_template('checkout.html', products=products, user_id=user_id)


@views.route('/thanks', methods=['GET'])
def thanks():
    id = session.get("id")
    if id == None:
        return redirect(url_for("views.login"))
    
    return render_template('order_confirm.html', id=id)


@views.route('/orders/<id>', methods=['GET'])
def orders(id):

    if id == None:
        return redirect(url_for("views.login"))
    
    products = get_orders_by_user_id(id)

    if products == None:
        return render_template('orders.html', products=[])

    return render_template('orders.html', products=products)


@views.route('/get_user_data/<id>', methods=['GET'])
def get_user_data(id):
    if id == None:
        return redirect(url_for("views.login"))
    
    current_directory = generate_excel_user_data(id)

    # Construct the file path using os.path.join and formatting the id
    file_path = os.path.join(current_directory, "database", "user_data", f"{id}.xlsx")

    # Send the Excel file as a downloadable attachment
    return send_file(file_path, as_attachment=True)


@views.route('/verify-password', methods=['POST'])
def verify_password():
    data = request.get_json()
    print(data)
    password = data.get('password')

    if not password:
        return jsonify({'error': 'Password not provided'}), 400

    # Check if the password has been breached
    count = check_password(password)
    
    if count > 0:
        return jsonify({'breached': True, 'count': count})
    else:
        return jsonify({'breached': False})