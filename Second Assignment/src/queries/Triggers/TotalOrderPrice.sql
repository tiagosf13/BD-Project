USE [BD-Project];
GO;

CREATE TRIGGER updateTotalOrderPrice ON PRODUCTS_ORDERED
AFTER INSERT, UPDATE
AS
BEGIN
    DECLARE @orderid as int;
    SELECT @orderid = Order_id from inserted;

    UPDATE ORDERS
    SET total_price = (
            SELECT sum(price * quantity) 
            FROM Products_ordered INNER JOIN Products
                ON Products_ordered.Product_Id = Products.Product_Id
            WHERE Order_id = @orderid
    ) WHERE Order_id = @orderid;
END
GO;

ENABLE TRIGGER updateTotalOrderPrice ON PRODUCTS_ORDERED;