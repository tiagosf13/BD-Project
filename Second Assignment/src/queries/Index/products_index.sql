use [p2g3]

-- otimizar search de product_id, product_name, product_category
CREATE INDEX IX_products_product_name ON products(product_name)
CREATE INDEX IX_products_product_category ON products(category)