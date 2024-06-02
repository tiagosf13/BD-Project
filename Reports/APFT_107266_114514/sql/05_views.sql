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
GO


DROP VIEW IF EXISTS CompleteUserData
GO

CREATE VIEW CompleteUserData AS
SELECT u.user_id, 
            u.username, 
            u.email, 
            o.order_id, 
            po.product_id, 
            po.quantity, 
            o.shipping_address, 
            o.order_date, 
            r.rating, 
            r.review_text
        FROM 
            users u
        LEFT OUTER JOIN 
            orders o ON u.user_id = o.user_id
        LEFT OUTER JOIN
            products_ordered po ON  po.order_id = o.order_id
        LEFT OUTER JOIN 
            reviews r ON u.user_id = r.user_id
GO

DROP VIEW IF EXISTS users_admin
Go

CREATE VIEW users_admin
AS
    SELECT *
    FROM users
    WHERE users.admin_role = 1
GO

DROP VIEW IF EXISTS users_clients
Go

CREATE VIEW users_clients
AS
    SELECT *
    FROM users
    WHERE users.admin_role = 0
GO