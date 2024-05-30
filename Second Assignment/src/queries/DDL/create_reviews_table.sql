USE [p2g3]

-- Check if the table exists -- Create the table if it does not exist
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'reviews')
BEGIN
    -- Table: public.reviews -- Table for storing product reviews data
    CREATE TABLE reviews (
        review_id INT NOT NULL CHECK(review_id > 0),
        product_id INT NOT NULL,
        user_id INT NOT NULL,
        review_text VARCHAR(255) NOT NULL,
        rating DECIMAL(2,1) NOT NULL CHECK(rating >= 0),
        review_date DATE NOT NULL,

        CONSTRAINT REVIEWS_PK
            PRIMARY KEY (review_id),
        
        CONSTRAINT REVIEWS_PK_product_id
            FOREIGN KEY (product_id) REFERENCES products(product_id),
        CONSTRAINT REVIEWS_PK_user_id
            FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
END

-- Path: src/queries/create_reviews_table.sql