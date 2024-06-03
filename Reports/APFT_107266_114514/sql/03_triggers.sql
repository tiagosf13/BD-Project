USE [p2g3];

DROP TRIGGER IF EXISTS deleteZeroItemsCart
GO

CREATE TRIGGER deleteZeroItemsCart ON dbo.carts
AFTER DELETE
AS
BEGIN
    DECLARE @userId as int;
    DECLARE @productId as int;
    SELECT @productId = product_id, @userId = user_id from deleted;

    IF (SELECT quantity 
        FROM dbo.carts
        WHERE user_id = @userId AND product_id = @productId) = 0
    BEGIN
        DELETE FROM carts
        WHERE user_id = @userId AND product_id = @productId
    END
END
GO

DROP TRIGGER IF EXISTS SingleReviewPerUser
GO

-- Trigger will run to guarantee that each user can only have one review
-- On each product, if a new review is made, review is simply overwritten
CREATE TRIGGER SingleReviewPerUser on dbo.REVIEWS
INSTEAD OF INSERT
AS
BEGIN
    declare @userID as int;
    declare @productID as int;
    declare @reviewText as VARCHAR(255);
    declare @rating as int;
    declare @reviewDate as DATE;

    select @userID = user_id, @productID = product_id, 
           @reviewText = review_text, @rating = rating, 
           @reviewDate = review_date
    FROM inserted;

    IF EXISTS (SELECT user_id FROM REVIEWS
                WHERE user_id = @userID AND product_id = @productID)
    BEGIN
        UPDATE REVIEWS
        SET review_text = @reviewText,
            rating = @rating, 
            review_date = @reviewDate
        WHERE user_id = @userID AND product_id = @productID;
    END
    ELSE
    BEGIN
        INSERT INTO reviews
        SELECT * FROM inserted;
    END
END
GO


DROP TRIGGER IF EXISTS updateTotalOrderPrice
GO

CREATE TRIGGER updateTotalOrderPrice ON dbo.PRODUCTS_ORDERED
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
    ) WHERE order_id = @orderid;
END