SELECT COUNT(*) FROM orders INDEXED BY idx_orders_created WHERE status = 'paid' AND created_on >= '2024-06-01';
