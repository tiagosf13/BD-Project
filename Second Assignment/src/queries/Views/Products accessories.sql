CREATE VIEW [Products accessories] AS
SELECT product_id, product_name, product_description, price, stock
FROM PRODUCTS
WHERE category = 'accessories' and available = 1 and stock > 0