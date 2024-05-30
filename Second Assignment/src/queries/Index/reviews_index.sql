-- otimizar search de product_id

CREATE CLUSTERED INDEX IX_reviews_product_id ON reviews(product_id)