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
        LEFT JOIN 
            orders o ON u.user_id = o.user_id
        LEFT JOIN
            products_ordered po ON  po.order_id = o.order_id
        LEFT JOIN 
            reviews r ON u.user_id = r.user_id