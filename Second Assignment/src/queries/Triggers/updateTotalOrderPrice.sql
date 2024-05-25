CREATE TRIGGER dbo.updateTotalOrderPrice ON dbo.PRODUCTS_ORDERED
AFTER INSERT, UPDATE
AS
BEGIN
    DECLARE @orderid as int;
    SELECT @orderid = Order_id from inserted;

    UPDATE ORDERS
    SET total_price = (
            SELECT sum(price * quantity) 
            FROM Products_ordered po 
			INNER JOIN Products p ON po.Product_Id = p.Product_Id
            WHERE po.Order_id = @orderid
    ) WHERE Order_id = @orderid;
END