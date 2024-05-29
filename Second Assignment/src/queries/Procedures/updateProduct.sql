USE [p2g3];

DROP PROCEDURE IF EXISTS updateProduct
GO

CREATE PROCEDURE updateProduct 
    @productID int = null,
    @productName VARCHAR(255) = null,
    @productDescription varchar(255) = null,
    @productPrice int = null,
    @productCategory varchar(255) = null,
    @productQuantity int = null
AS
BEGIN
    IF NOT EXISTS (SELECT product_id from PRODUCTS where product_id=@productID)
    BEGIN
        RAISERROR ('Product not found!', 1, 1);
        RETURN
    END

    BEGIN TRANSACTION
        IF (@productName is not null)
        BEGIN 
            UPDATE PRODUCTS
            SET product_name = @productName
            WHERE product_id = @productID
        END

        IF (@productDescription is not null)
        BEGIN 
            UPDATE PRODUCTS
            SET product_description = @productDescription
            WHERE product_id = @productID
        END

        IF (@productCategory is not null)
        BEGIN 

            UPDATE PRODUCTS
            SET category = @productCategory
            WHERE product_id = @productID
        END



        IF (@productQuantity is not null)
        BEGIN 
            IF (@productQuantity < 0)
            BEGIN
                RAISERROR ('Quantity cannot be below zero!', 8, 1)
                ROLLBACK TRANSACTION;
                RETURN
            END

            UPDATE PRODUCTS
            SET stock = @productQuantity
            WHERE product_id = @productID
        END

        IF (@productPrice is not null)
        BEGIN 
            IF (@productPrice < 0)
            BEGIN
                RAISERROR ('Quantity cannot be below zero!', 8, 1)
                ROLLBACK TRANSACTION;
                RETURN
            END

            UPDATE PRODUCTS
            SET price = @productPrice
            WHERE product_id = @productID
        END
    COMMIT TRANSACTION
END