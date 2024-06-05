USE [p2g3];

DROP VIEW IF EXISTS Available_Products
GO

-- View Made to serve Users
-- Only admins should have all products available to view
CREATE VIEW Available_Products
AS
    SELECT product_id, product_name, product_description, price, category, stock
    FROM products
    WHERE available = 1 AND stock > 0