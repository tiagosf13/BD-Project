use [p2g3]

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