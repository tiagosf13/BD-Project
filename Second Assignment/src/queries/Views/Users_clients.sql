-- TODO
use [p2g3]

DROP VIEW IF EXISTS users_clients
Go

CREATE VIEW users_clients
AS
    SELECT *
    FROM users
    WHERE users.admin_role = 0
GO