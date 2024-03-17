USE [BD-Project]

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

-- Path: src/queries/create_products_table.sql