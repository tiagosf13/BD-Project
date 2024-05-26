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
    order_date date,
    product_id int,
    product_name varchar(255),
    category VARCHAR(255),
    price DECIMAL(10, 2),
    quantity int,
    total_price DECIMAL(10, 2),
    available bit,
    reviewed bit DEFAULT 0
)
AS
BEGIN
    INSERT INTO @result(
        order_id, order_date, product_id, product_name, category, price, quantity, total_price, available
    )
    SELECT o.order_id, o.order_date, p.product_id, p.product_name, p.category, p.price, po.quantity, o.total_price, p.available
    FROM (ORDERS as o
        INNER JOIN PRODUCTS_ORDERED as po
            ON o.order_id = po.order_id)
        INNER JOIN PRODUCTS as p
            ON po.product_id = p.product_id
    WHERE user_id = @userID

    UPDATE @result
    SET reviewed = 1
    WHERE product_id in (SELECT product_id FROM reviews WHERE user_id = @userID)
    
    RETURN
END