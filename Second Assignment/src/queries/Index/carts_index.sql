use [p2g3]
-- Optimizar search de user_id
CREATE CLUSTERED INDEX IX_carts_user_id ON carts(user_id) 