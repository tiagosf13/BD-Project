USE [p2g3]

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