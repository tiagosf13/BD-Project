use [p2g3]
GO

DROP VIEW IF EXISTS users_admin
Go

CREATE VIEW users_admin
AS
    SELECT *
    FROM users
    WHERE users.admin_role = 1
GO