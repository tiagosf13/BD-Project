CREATE FUNCTION getProductById (@productID int) RETURNS TABLE
RETURN (
    SELECT products.*, p.avgRating
    FROM products INNER JOIN (
            SELECT p.product_id, 
                COALESCE(AVG(CAST(rating AS DECIMAL(2, 1))), 0.0) as avgRating
            FROM products as p LEFT JOIN reviews as r
                ON p.product_id = r.product_id
            WHERE p.product_id= 5060
            GROUP BY p.product_id
    ) as p ON products.product_id = p.product_id
)