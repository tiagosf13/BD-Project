USE [p2g3]

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
        
        CONSTRAINT USERS_PK
            PRIMARY KEY (user_id),
    );

    -- Null User -> To be used when an account gets deleted
    INSERT INTO users
    VALUES (
        -1,                 -- ID
        '[DELETED USER]',   -- username
        'null',             -- hashed_password
         null,              -- password_reset_token
         null,              -- password_reset_token_timestamp
        'null',             -- email
        'null',             -- totp_secret_key
        '1970-01-01',       -- totp_secret_key_timestamp
        0                   -- admin_role
    )
END
-- otimizar search de user_id e username
CREATE INDEX IX_users_username ON users(username)



-- Check if the table exists -- Create the table if it does not exist
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'emergency_codes')
BEGIN
    -- Table: public.emergency_codes -- Table for storing emergency codes data
    CREATE TABLE emergency_codes (
        user_id INT NOT NULL,
        emergency_code INT NOT NULL,
        emergency_code_valid BIT NOT NULL,
        emergency_code_timestamp DATETIMEOFFSET NOT NULL,

        CONSTRAINT EMERGENCY_CODES_PK 
            PRIMARY KEY (user_id, emergency_code),

        CONSTRAINT EMERGENCY_CODES_FK_user_id
            FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
END

-- Check if the table exists -- Create the table if it does not exist
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'products')
BEGIN
    -- Table: public.products -- Table for storing products data
    CREATE TABLE products (
        product_id INT NOT NULL CHECK (product_id > 0),
        product_name VARCHAR(255) NOT NULL,
        product_description VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2) NOT NULL CHECK(price >= 0),
        category VARCHAR(255) NOT NULL,
        stock INT NOT NULL CHECK(stock >= 0),
        available BIT NOT NULL,

        CONSTRAINT PRODUCTS_PK
            PRIMARY KEY (product_id)
    );
END
-- otimizar search de product_id, product_name, product_category
CREATE INDEX IX_products_product_name ON products(product_name)
CREATE INDEX IX_products_product_category ON products(category)



-- Check if the table exists -- Create the table if it does not exist
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'reviews')
BEGIN
    -- Table: public.reviews -- Table for storing product reviews data
    CREATE TABLE reviews (
        product_id INT NOT NULL,
        user_id INT NOT NULL,
        review_text VARCHAR(255) NOT NULL,
        rating DECIMAL(2,1) NOT NULL CHECK(rating >= 0),
        review_date DATE NOT NULL,

        CONSTRAINT REVIEWS_PK
            PRIMARY KEY (product_id, user_id),
        
        CONSTRAINT REVIEWS_PK_product_id
            FOREIGN KEY (product_id) REFERENCES products(product_id),
        CONSTRAINT REVIEWS_PK_user_id
            FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
END
-- otimizar search de product_id



-- Check if the table exists -- Create the table if it does not exist
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'orders')
BEGIN
    -- Table: public.orders -- Table for storing order data
    CREATE TABLE orders (
        order_id INT NOT NULL,
        user_id INT NOT NULL,
        total_price DECIMAL(10, 2) NOT NULL CHECK(total_price >= 0),
        shipping_address VARCHAR(255) NOT NULL,
        order_date DATETIMEOFFSET NOT NULL,
        
        CONSTRAINT ORDERS_PK
            PRIMARY KEY (order_id),
            
        CONSTRAINT ORDERS_FK_user_id
            FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
END
-- Optimizar search de user_id
CREATE INDEX IX_orders_user_id ON orders(user_id)



-- Check if the table exists -- Create the table if it does not exist
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'products_ordered')
BEGIN
    -- Table: public.products_ordered -- Table for storing ordered products data
    CREATE TABLE products_ordered (
        order_id INT NOT NULL,
        product_id INT NOT NULL,
        quantity INT NOT NULL  CHECK(quantity > 0),

        CONSTRAINT PRODUCTS_ORDERED_PK
            PRIMARY KEY (order_id, product_id),
        
        CONSTRAINT PRODUCTS_ORDERED_PK_order_id
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
        CONSTRAINT PRODUCTS_ORDERED_PK_product_id
            FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
END



-- Check if the table exists -- Create the table if it does not exist
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'carts')
BEGIN
    -- Table: public.carts -- Table for storing cart data
    CREATE TABLE carts (
        user_id INT NOT NULL,
        product_id INT NOT NULL,
        quantity INT NOT NULL CHECK(quantity >= 0),

        CONSTRAINT CARTS_PK 
            PRIMARY KEY (user_id, product_id),
            
        CONSTRAINT CARTS_FK_user_id
            FOREIGN KEY (user_id) REFERENCES users(user_id),
        CONSTRAINT CARTS_FK_product_id
            FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
END