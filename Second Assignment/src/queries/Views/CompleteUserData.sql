CREATE OR REPLACE VIEW CompleteUserData AS
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
        INNER JOIN 
            orders o ON u.user_id = o.user_id
        INNER JOIN
            products_ordered po ON  po.order_id = o.order_id
        INNER JOIN 
            reviews r ON u.user_id = r.user_id