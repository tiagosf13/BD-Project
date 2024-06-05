-- otimizar search de product_id

CREATE INDEX IX_reviews_product_id ON reviews(product_id)