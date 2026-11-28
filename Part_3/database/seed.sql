-- ==============================================================================
-- SAIGONBITE CLOUD KITCHEN MULTI-BRAND DELIVERY HUB
-- Sample Seed Data (DML) for Part 3 Implementation & Live Demo
-- ==============================================================================

USE saigonbite_db;

INSERT INTO hubs (hub_id, hub_name, address, latitude, longitude, max_capacity_orders, is_busy) VALUES
('H01', 'SaigonBite Hub District 1', '123 Nguyen Hue, District 1, HCMC', 10.7745000, 106.7035000, 50, FALSE),
('H02', 'SaigonBite Hub District 7', '456 Nguyen Van Linh, District 7, HCMC', 10.7295000, 106.7155000, 40, TRUE);

INSERT INTO kitchen_stations (station_id, hub_id, station_name, station_type, current_load_orders, capacity_limit) VALUES
('ST-H01-GRILL', 'H01', 'Hub 1 Grill & Wok Station', 'Grill', 6, 15),
('ST-H01-DRINK', 'H01', 'Hub 1 Beverage Station', 'Drink_Dessert', 4, 15),
('ST-H02-GRILL', 'H02', 'Hub 2 Grill & Wok Station', 'Grill', 14, 15);

INSERT INTO brands (brand_id, brand_name, cuisine_type, status) VALUES
('BR-01', 'Pho Saigon Heritage', 'Vietnamese', 'ACTIVE'),
('BR-02', 'K-Bowl Express', 'Korean', 'ACTIVE');

INSERT INTO menu_items (item_id, brand_id, item_name, description, unit_price, is_available, station_type) VALUES
('MI-01', 'BR-01', 'Pho Bo Dac Biet / Special Beef Pho', 'Traditional beef noodle soup', 85000.00, TRUE, 'Grill'),
('MI-02', 'BR-02', 'Spicy Chicken Kimbap', 'Korean grilled chicken rice roll', 65000.00, TRUE, 'Grill'),
('MI-03', 'BR-01', 'Tra Dao Cam Sa / Peach Lemongrass Tea', 'Refreshing iced tea', 35000.00, TRUE, 'Drink_Dessert');

INSERT INTO customers (customer_id, full_name, customer_type) VALUES
('CUS-01', 'Nguyen Minh Anh', 'Local'),
('CUS-02', 'John Miller', 'Foreign');

INSERT INTO local_customers (customer_id, phone_number, preferred_language) VALUES
('CUS-01', '+84901234567', 'vi');

INSERT INTO foreign_tourists (customer_id, passport_number, email_address, preferred_language) VALUES
('CUS-02', 'US8942105', 'john.miller@example.com', 'en');

INSERT INTO vouchers (voucher_code, discount_percent, max_discount_amount, min_order_amount, start_date, end_date, usage_limit, used_count, status) VALUES
('SBWELCOME10', 10.00, 50000.00, 100000.00, '2026-11-01 00:00:00', '2026-12-31 23:59:59', 200, 12, 'ACTIVE'),
('QUIET10', 10.00, 40000.00, 100000.00, '2026-11-01 00:00:00', '2026-12-31 23:59:59', 500, 5, 'ACTIVE');

INSERT INTO shippers (shipper_id, full_name, phone_number, vehicle_plate, current_status, wallet_balance) VALUES
('SHP-01', 'Tran Van Binh', '+84912345678', '59-X1 12345', 'AVAILABLE', 450000.00);

INSERT INTO orders (order_id, customer_id, hub_id, voucher_code, order_time, order_status, delivery_address, distance_km, subtotal, delivery_fee, discount_amount, final_total, payment_method, payment_status) VALUES
('ORD-001', 'CUS-01', 'H01', 'SBWELCOME10', '2026-11-26 11:30:00', 'Pending_Kitchen', '45 Le Loi, District 1, HCMC', 3.20, 185000.00, 21000.00, 18500.00, 187500.00, 'Card', 'SUCCESS'),
('ORD-002', 'CUS-02', 'H01', NULL, '2026-11-26 11:35:00', 'Pending_Kitchen', 'Rex Hotel, 141 Nguyen Hue, District 1', 1.50, 150000.00, 15000.00, 0.00, 165000.00, 'COD', 'PENDING');

INSERT INTO order_lines (order_line_id, order_id, item_id, quantity, unit_price, subtotal) VALUES
('OL-001', 'ORD-001', 'MI-01', 1, 85000.00, 85000.00),
('OL-002', 'ORD-001', 'MI-02', 1, 65000.00, 65000.00),
('OL-003', 'ORD-001', 'MI-03', 1, 35000.00, 35000.00),
('OL-004', 'ORD-002', 'MI-01', 1, 85000.00, 85000.00),
('OL-005', 'ORD-002', 'MI-02', 1, 65000.00, 65000.00);

INSERT INTO kitchen_tickets (ticket_id, order_id, station_id, ticket_status, estimated_cook_time_mins, started_at) VALUES
('KT-001', 'ORD-001', 'ST-H01-GRILL', 'QUEUED', 15, NULL);

INSERT INTO payments (payment_id, order_id, payment_method, amount, status, transaction_ref, paid_at) VALUES
('PAY-001', 'ORD-001', 'Card', 187500.00, 'SUCCESS', 'TXN-20261126-001', '2026-11-26 11:30:05'),
('PAY-002', 'ORD-002', 'COD', 165000.00, 'PENDING', NULL, NULL);

INSERT INTO audit_logs (action_name, entity_name, entity_id, performed_by, details) VALUES
('SEED_INITIALIZATION', 'System', 'INIT', 'Administrator', 'Initial Part 3 demo dataset loaded.');
