USE [p2g3];

DROP PROCEDURE IF EXISTS deleteUser
GO

-- Create the stored procedure in the specified schema
CREATE PROCEDURE deleteUser @userID int
AS
BEGIN
    IF NOT EXISTS (SELECT * FROM users where User_id = @userID)
    BEGIN
        RAISERROR('User not found!', 0, 1);
    END
    
    BEGIN TRANSACTION
        BEGIN TRY
            -- Replace all orders and reviews with null user
            UPDATE orders
            SET User_id = -1
            WHERE User_id = @userID
            
            UPDATE reviews
            SET User_id = -1
            WHERE User_id = @userID

            -- Delete existence of original user
            DELETE FROM emergency_codes
            WHERE User_id = @userID

            DELETE FROM carts
            WHERE User_id = @userID

            DELETE FROM users
            WHERE User_id = @userID
        END TRY

        BEGIN CATCH
            RAISERROR('Something went wrong while deleting user!', 16, 1);
            ROLLBACK;
        END CATCH

    COMMIT TRANSACTION;
END
GO

DROP PROCEDURE IF EXISTS updateAccount
GO

CREATE PROCEDURE updateAccount
    @userId int,
    @username varchar(255),
    @email varchar(255),
    @password varchar(255)
AS
BEGIN
    IF NOT EXISTS (SELECT user_id from users where user_id=@userID)
    BEGIN
        RAISERROR ('User not found!', 1, 1);
        RETURN
    END

    BEGIN TRANSACTION
        IF (@password != '')
        BEGIN
            UPDATE USERS
            SET hashed_password = @password
            WHERE user_id = @userId
        END
        
        IF (@username != '')
        BEGIN
            IF EXISTS (SELECT username from users where username = @username)
            BEGIN
                RAISERROR ('Username already in use!', 1, 1);
                ROLLBACK TRANSACTION
                RETURN
            END
            UPDATE USERS
            SET username = @username
            WHERE user_id = @userId
        END

        IF (@email != '')
        BEGIN
            IF EXISTS (SELECT email from users where email = @email)
            BEGIN
                RAISERROR ('Email already in use!', 1, 1);
                ROLLBACK TRANSACTION
                RETURN
            END
            UPDATE USERS
            SET email = @email
            WHERE user_id = @userId
        END
    COMMIT TRANSACTION
END
GO

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
GO

-- UDF's

DROP FUNCTION IF EXISTS getMonthlySalesTable
GO
-- OPTIONAL PARAMS month(int), year(int)
-- If month AND year are passed; then 
--      Returns a table with month-year total sale
-- Else If no parameters are passed
--      Returns table with overall sales divided monthly
CREATE FUNCTION getMonthlySalesTable(@month int = null, @year int = null)
RETURNS @monthlySales TABLE (
    year        int,
    month       int,
    total_sales  DECIMAL(10,2)
)
AS
BEGIN
    IF (@month is not null AND @year is not null)
    BEGIN
        INSERT INTO @monthlySales
        SELECT year, month, sum(total_price) as total_sales
        FROM (
            SELECT order_id,
                    YEAR(order_date) as year,
                    MONTH(order_date) as month,
                    total_price
            FROM ORDERS
        ) ordersMade
        GROUP BY year, month
        HAVING month=@month AND year=@year
    END

    ELSE
    BEGIN
        INSERT INTO @monthlySales
        SELECT year, month, sum(total_price) as total_sales
        FROM (
            SELECT order_id,
                    YEAR(order_date) as year,
                    MONTH(order_date) as month,
                    total_price
            FROM ORDERS
        ) ordersMade
        GROUP BY year, month
    END
    RETURN
END
GO

DROP FUNCTION IF EXISTS getProductById
GO

CREATE FUNCTION getProductById (@productID int) RETURNS TABLE
RETURN (
    SELECT products.*, p.avgRating
    FROM products INNER JOIN (
            SELECT p.product_id, 
                COALESCE(AVG(CAST(rating AS DECIMAL(2, 1))), 0.0) as avgRating
            FROM products as p LEFT JOIN reviews as r
                ON p.product_id = r.product_id
            WHERE p.product_id= @productID
            GROUP BY p.product_id
    ) as p ON products.product_id = p.product_id
)
GO

DROP FUNCTION IF EXISTS getUserCart
GO

CREATE FUNCTION getUserCart(@userID int) RETURNS TABLE
RETURN (
    SELECT products.product_id, quantity, products.product_name, products.price
    FROM carts INNER JOIN products 
        ON carts.product_id = products.product_id
    WHERE user_id=@userID
)
GO

DROP FUNCTION IF EXISTS getUserOrders
GO

-- Get all orders made by a user with all the products
-- and whether a review as been made for each product
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
GO

DROP FUNCTION IF EXISTS isAdmin
GO

CREATE FUNCTION isAdmin (@userID int) RETURNS BIT
AS
BEGIN
    IF EXISTS (SELECT * FROM Users_admin WHERE user_id = @userID)
    BEGIN
        RETURN 1
    END
    RETURN 0
END
GO

DROP FUNCTION IF EXISTS searchAvailableProducts
GO

CREATE FUNCTION searchAvailableProducts (
    @searchTerm VARCHAR(255) = '%',
    @category VARCHAR(255) = '%',
    @minPrice int = 0,
    @maxPrice int = 1000000
) RETURNS TABLE
AS
RETURN (
    SELECT * 
    FROM Available_Products
    WHERE (product_name LIKE @searchTerm OR
           product_id LIKE @searchTerm) 
        AND category LIKE @category 
        AND price BETWEEN @minPrice AND @maxPrice
)