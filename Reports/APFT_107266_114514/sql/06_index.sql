use [p2g3]

-- Optimizar search de user_id
CREATE INDEX IX_orders_user_id ON orders(user_id)

-- otimizar search de product_id, product_name, product_category
CREATE INDEX IX_products_product_name ON products(product_name)
CREATE INDEX IX_products_product_category ON products(category)

-- otimizar search de product_id
CREATE INDEX IX_reviews_product_id ON reviews(product_id)

-- otimizar search de user_id e username
CREATE INDEX IX_users_username ON users(username)