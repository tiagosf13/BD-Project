use [p2g3]

-- otimizar search de product_id, product_name, product_category
CREATE CLUSTERED INDEX IX_products_product_id ON products(product_id)
CREATE INDEX IX_products_product_name ON products(product_name)
CREATE INDEX IX_products_product_category ON products(product_category)