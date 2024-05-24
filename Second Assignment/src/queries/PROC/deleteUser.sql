use [BD-Project];
GO;

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