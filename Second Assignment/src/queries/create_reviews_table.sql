USE [BD-Project]

-- Check if the table exists -- Create the table if it does not exist
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'reviews')
BEGIN
    -- Table: public.reviews -- Table for storing product reviews data
    CREATE TABLE reviews (
        review_id INT NOT NULL,
        product_id INT NOT NULL,
        user_id INT NOT NULL,
        review_text VARCHAR(255) NOT NULL,
        rating DECIMAL(2,1) NOT NULL,
        review_date DATE NOT NULL,
        PRIMARY KEY (review_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
END

-- Path: src/queries/create_reviews_table.sql