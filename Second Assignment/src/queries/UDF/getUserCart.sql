CREATE FUNCTION getUserCart(@userID int) RETURNS TABLE
RETURN (
    SELECT products.product_id, quantity, products.product_name, products.price
    FROM carts INNER JOIN products 
        ON carts.product_id = products.product_id
    WHERE user_id=@userID
)