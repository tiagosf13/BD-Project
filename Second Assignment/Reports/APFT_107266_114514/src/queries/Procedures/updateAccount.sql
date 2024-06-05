USE [p2g3];

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