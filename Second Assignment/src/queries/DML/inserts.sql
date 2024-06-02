-- Insert a product --
-- ProductManagement:create_product --
INSERT INTO products (product_id, product_name, product_description, price, category, stock, available)
VALUES (?, ?, ?, ?, ?, ?, ?);


-- Insert a review --
-- ProductManagement:create_review --
INSERT INTO reviews (review_id, product_id, user_id, review_text, rating, review_date) 
VALUES (?, ?, ?, ?, ?, ?);


-- Register an order, creating the order and then adding the products ordered --
-- OrderManagement:register_order --
INSERT INTO orders (order_id, user_id, total_price, shipping_address, order_date)
VALUES (?, ?, ?, ?, ?);
INSERT INTO products_ordered (order_id, product_id, quantity)
VALUES (?, ?, ?);


-- Store a new emergency code --
-- TOTPHandler:store_emergency_codes --
INSERT INTO emergency_codes (user_id, emergency_code, emergency_code_valid, emergency_code_timestamp) VALUES (?, ?, ?, ?);


-- Register a new user --
-- UserManagement:create_user --
INSERT INTO users (user_id, username, hashed_password, email, totp_secret_key, totp_secret_key_timestamp, admin_role) VALUES (?, ?, ?, ?, ?, ?, ?);
