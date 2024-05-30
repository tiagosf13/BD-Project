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