-- Get all orders made by a user with all the products
-- and whether a review as been made for each product
-- Podemos apresentar tipo
--  -> Order 1
--       |-> Produto 1 (preço unitario) ---- Quantidade ---- Preço total ---- Review feita
--       |-> Produto 2 (preço unitario) ---- Quantidade ---- Preço total ---- Review feita
--       |-> Produto 3 (preço unitario) ---- Quantidade ---- Preço total ---- Botao Adicionar review
--       |-> Produto 4 (preço unitario) ---- Quantidade ---- Preço total ---- Review feita
CREATE FUNCTION getUserOrders(@userID int) RETURNS @result TABLE (
    order_id int,
    product_id int,
    quantity int,
    price money,
    reviewed bit
)
AS
BEGIN
    INSERT INTO @result(
        order_id, product_id, quantity, price
    )
    SELECT PRODUCTS_ORDERED.order_id, PRODUCTS_ORDERED.product_id, PRODUCTS_ORDERED.quantity, PRODUCTS.price
    FROM (ORDERS 
        INNER JOIN PRODUCTS_ORDERED 
            ON ORDERS.order_id = PRODUCTS_ORDERED.order_id)
        INNER JOIN PRODUCTS
            ON PRODUCTS_ORDERED.product_id = PRODUCTS.product_id

    UPDATE @result
    SET reviewed = 1
    WHERE EXISTS (SELECT * FROM reviews WHERE product_id = @productID AND user_id = @userID) 
    
    RETURN
END