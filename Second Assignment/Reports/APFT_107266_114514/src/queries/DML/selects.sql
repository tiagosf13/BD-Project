-- Get the Username Based on the User ID --
-- EmailHandler:get_username_by_idc--
SELECT username FROM users WHERE user_id = ?;


-- Get the Products, their quantity in the Cart and the total price for that item, based on the User ID --
-- EmailHandler:sql_to_pdf --
SELECT carts.product_id, carts.quantity, products.product_name, products.price, carts.quantity * products.price AS total
FROM carts
    JOIN products ON carts.product_id = products.product_id
WHERE carts.user_id = ?;


-- Verify if there is a product with the given name --
-- EmailHandler:verify_product_exists --
SELECT product_id FROM products WHERE product_name = ?;


-- Verify if the product is available --
-- EmailHandler:check_product_availability --
SELECT available FROM products WHERE product_id = ?;


-- Get a product's quantity in the cart --
-- ProductManagement:get_cart_quantity --
SELECT quantity FROM carts WHERE user_id = ? AND product_id = ?;


-- Add or Remove a quantity of the product to the cart, inserting if not exists, updating if it does --
-- ProductManagement:set_cart_item --
SELECT * FROM carts WHERE product_id = ? AND user_id = ?;

UPDATE carts SET quantity = quantity + ? 
WHERE product_id = ? AND user_id = ?;

UPDATE carts SET quantity = quantity - ? 
WHERE product_id = ? AND user_id = ?;

INSERT INTO carts (product_id, quantity, user_id)
VALUES (?, ?, ?);


-- Get the products that correspod to the given filters used by the client, first for a regular client, second to a admin -- 
-- We used wildcars --
-- search_term = f"%{search_term}%" --
-- category = f"%{category}%" --
-- Retrievers:get_all_products --
SELECT * 
FROM searchAvailableProducts (?, ?, ?, ?)
ORDER BY price {sort_order};

SELECT * 
FROM products
WHERE (product_name LIKE ? OR product_id LIKE ?)
    AND category LIKE ? 
    AND price BETWEEN ? AND ? 
    AND available = ?
ORDER BY price {sort_order};


-- Get a product by its ID --
-- Retrievers:get_product_by_id --
SELECT * FROM getProductById(?);


-- Get the reviews for a product --
-- Retrievers:get_product_reviews --
SELECT * FROM reviews WHERE product_id = ?;


-- Check if a product is available --
-- Retrievers:check_product_availability --
SELECT available FROM products WHERE product_id = ?;


-- Get a user's cart --
-- Retrievers:get_cart --
SELECT * FROM getUserCart(?);


-- Get the monthly sales --
-- Retrievers:get_monthly_sales --
SELECT * FROM getMonthlySalesTable(?, ?);


-- Check if a emergency code is exists --
-- TOTPHandler:check_existence_emergency_codes --
SELECT CASE WHEN EXISTS (SELECT 1 FROM emergency_codes WHERE user_id = ?) THEN 1 ELSE 0 END AS user_exists;


-- Search for a user, generalized query --
-- UserManagement:search_user --
SELECT {select_attribute} FROM users WHERE {search_regex} = ?;


-- Check if the UserID exists --
-- UserManagement:check_id_existence --
IF EXISTS(SELECT 1 FROM users WHERE user_id = ?) SELECT 1 ELSE SELECT 0;


-- Get the orders for a user --
-- UserManagement:get_orders_by_user_id --
SELECT * from getUserOrders(?);


-- Check if a user bought a product --
-- UserManagement:check_user_bought_product --
SELECT products_ordered.order_id 
FROM products_ordered 
    JOIN orders ON products_ordered.order_id = orders.order_id
WHERE orders.user_id = ? AND products_ordered.product_id = ?;


-- Get all the user's data --
-- UserManagement:get_user_data_by_id --
SELECT *
FROM CompleteUserData
WHERE user_id = ?;


-- Check if the username exists --
-- Verifiers:check_username_exists --
SELECT CASE WHEN EXISTS (SELECT 1 FROM users WHERE username = ?) THEN 1 ELSE 0 END;


-- Check if product in cart --
-- Verifiers:check_product_in_cart --
SELECT COUNT(*) FROM carts WHERE product_id=? AND user_id=?;
