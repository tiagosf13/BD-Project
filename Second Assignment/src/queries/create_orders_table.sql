USE [BD-Project]

-- Check if the table exists -- Create the table if it does not exist
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'orders')
BEGIN
    -- Table: public.orders -- Table for storing order data
    CREATE TABLE orders (
        order_id INT NOT NULL,
        user_id INT NOT NULL,
        total_price DECIMAL(10, 2) NOT NULL,
        shipping_address VARCHAR(255) NOT NULL,
        order_date DATETIMEOFFSET NOT NULL,
        PRIMARY KEY (order_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
END

-- Path: src/queries/create_orders_table.sql
