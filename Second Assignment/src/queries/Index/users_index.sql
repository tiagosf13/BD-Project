use [p2g3]

-- otimizar search de user_id e username
CREATE INDEX IX_users_username ON users(username)