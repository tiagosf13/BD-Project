use [p2g3]

-- otimizar search de user_id e username
CREATE CLUSTERED INDEX IX_users_user_id ON users(user_id)
CREATE INDEX IX_users_username ON users(username)