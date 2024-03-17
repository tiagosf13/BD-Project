USE [BD-Project]

-- Check if the table exists -- Create the table if it does not exist
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'users')
BEGIN
    -- Table: public.users -- Table for storing user data
    CREATE TABLE users (
        user_id INT NOT NULL,
        username VARCHAR(255) NOT NULL,
        hashed_password VARCHAR(255) NOT NULL,
        password_reset_token VARCHAR(255),
        password_reset_token_timestamp DATETIMEOFFSET,
        email VARCHAR(255) NOT NULL,
        totp_secret_key VARCHAR(255) NOT NULL,
        totp_secret_key_timestamp DATETIMEOFFSET NOT NULL,
        admin_role BIT NOT NULL,
        PRIMARY KEY (user_id),
    );
END

-- Check if the table exists -- Create the table if it does not exist
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'products')
BEGIN
    -- Table: public.products -- Table for storing products data
    CREATE TABLE products (
        product_id INT NOT NULL,
        product_name VARCHAR(255) NOT NULL,
        product_description VARCHAR(255) NOT NULL,
        price MONEY NOT NULL,
        category VARCHAR(255) NOT NULL,
        stock INT NOT NULL,
        PRIMARY KEY (product_id)
    );
END

-- Check if the table exists -- Create the table if it does not exist
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'emergency_codes')
BEGIN
    -- Table: public.emergency_codes -- Table for storing emergency codes data
    CREATE TABLE emergency_codes (
        emergency_codes_set_id INT NOT NULL,
        user_id INT NOT NULL,
        emergency_code INT NOT NULL,
        emergency_code_valid BIT NOT NULL,
        emergency_codes_set_timestamp DATETIMEOFFSET NOT NULL,
        PRIMARY KEY (emergency_codes_set_id, user_id, emergency_code),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
END

USE [BD-Project]

-- Check if the table exists -- Create the table if it does not exist
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'carts')
BEGIN
    -- Table: public.carts -- Table for storing cart data
    CREATE TABLE carts (
        cart_id INT NOT NULL,
        user_id INT NOT NULL,
        product_id INT NOT NULL,
        quantity INT NOT NULL,
        PRIMARY KEY (cart_id, user_id, product_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
END

-- Check if the table exists -- Create the table if it does not exist
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'reviews')
BEGIN
    -- Table: public.reviews -- Table for storing product reviews data
    CREATE TABLE reviews (
        review_id INT NOT NULL,
        product_id INT NOT NULL,
        user_id INT NOT NULL,
        review_text VARCHAR(255) NOT NULL,
        rating INT NOT NULL,
        review_date DATE NOT NULL,
        PRIMARY KEY (review_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
END

-- Check if the table exists -- Create the table if it does not exist
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'orders')
BEGIN
    -- Table: public.orders -- Table for storing order data
    CREATE TABLE orders (
        order_id INT NOT NULL,
        user_id INT NOT NULL,
        product_id INT NOT NULL,
        quantity INT NOT NULL,
        total_price MONEY NOT NULL,
        shipping_address VARCHAR(255) NOT NULL,
        order_date DATETIMEOFFSET NOT NULL,
        PRIMARY KEY (order_id, user_id, product_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
END