-- Make a product unavailable, removing it from any cart and marking it as unavailable --
-- ProductManagement:remove_product --
DELETE FROM carts WHERE product_id = ?;
UPDATE products SET available = 0 WHERE product_id = ?;


-- Remove a product from the cart --
-- ProductManagement:remove_product_from_cart --
DELETE FROM carts WHERE product_id = ? AND user_id = ?;


-- Remove all products from the cart --
-- ProductManagement:remove_all_products_from_cart --
DELETE FROM carts WHERE user_id = ?;


-- Delete all emergency codes for a user --
-- TOTPHandler:store_emergency_codes --
DELETE FROM emergency_codes WHERE user_id = ?;