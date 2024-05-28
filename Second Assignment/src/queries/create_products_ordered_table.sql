USE [p2g3]

-- Check if the table exists -- Create the table if it does not exist
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'products_ordered')
BEGIN
    -- Table: public.products_ordered -- Table for storing ordered products data
    CREATE TABLE products_ordered (
        order_id INT NOT NULL,
        product_id INT NOT NULL,
        quantity INT NOT NULL,
        PRIMARY KEY (order_id, product_id),
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
END

-- Path: src/queries/create_products_ordered_table.sql