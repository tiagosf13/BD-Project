-- otimizar search de user_id e order_id
use [p2g3]

-- Optimizar search de user_id
CREATE CLUSTERED INDEX IX_orders_user_id ON orders(user_id)
CREATE INDEX IX_orders_order_id ON orders(order_id)