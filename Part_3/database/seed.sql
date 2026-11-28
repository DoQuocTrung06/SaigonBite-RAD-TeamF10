-- ==============================================================================
-- SAIGONBITE CLOUD KITCHEN MULTI-BRAND DELIVERY HUB (OFDH)
-- iii. Sample Data (DML) for Part 3 Implementation & Live Demo (Section 4.3.4)
-- Covers all 6 Main Use Cases: UC15, UC7, UC3, UC14, UC10, UC16
-- Authors: 524H0132, 524H0031, 524H0136
-- ==============================================================================

USE saigonbite_db;

-- 1. Hubs (H01 at 30% quiet load < 40% eligible for 10% Quiet-Kitchen discount; H02 at 88% busy load >= 85%)
INSERT INTO hubs (hub_id, hub_name, address, latitude, longitude, max_capacity_orders, hub_status, is_busy) VALUES
('H01', 'SaigonBite Hub District 1', '123 Nguyen Hue, District 1, HCMC', 10.7745000, 106.7035000, 50, 'Open', FALSE),
('H02', 'SaigonBite Hub District 7', '456 Nguyen Van Linh, District 7, HCMC', 10.7295000, 106.7155000, 40, 'Busy', TRUE);

-- 2. Kitchen Stations (Wok, Fryer, Assembly, Beverage at H01 & H02)
INSERT INTO kitchen_stations (station_id, hub_id, station_name, station_type, current_load_orders, capacity_limit) VALUES
('ST-H01-WOK', 'H01', 'District 1 Wok & Noodle Station', 'Wok', 5, 15),
('ST-H01-FRY', 'H01', 'District 1 Crispy Fryer Station', 'Fryer', 3, 15),
('ST-H01-ASM', 'H01', 'District 1 Salad & Banh Mi Assembly', 'Assembly', 4, 15),
('ST-H01-BEV', 'H01', 'District 1 Specialty Beverage Bar', 'Beverage', 3, 15),
('ST-H02-WOK', 'H02', 'District 7 Wok Station', 'Wok', 14, 15),
('ST-H02-BEV', 'H02', 'District 7 Beverage Station', 'Beverage', 12, 15);

-- 3. Virtual Restaurant Brands (UC14 — Author: 524H0031)
INSERT INTO brands (brand_id, brand_name, cuisine_type, status) VALUES
('BR-01', 'Pho Saigon Heritage', 'Vietnamese Traditional', 'Active'),
('BR-02', 'Saigon Crispy Banh Mi & Rolls', 'Vietnamese Street Food', 'Active'),
('BR-03', 'GreenBowl Tropical Salads & Tea', 'Healthy & Beverage', 'Active');

-- 4. Brand-to-Hub Assignments (UC14 — Author: 524H0031)
INSERT INTO brand_hubs (brand_id, hub_id) VALUES
('BR-01', 'H01'),
('BR-01', 'H02'),
('BR-02', 'H01'),
('BR-03', 'H01'),
('BR-03', 'H02');

-- 5. Bilingual Menu Items (UC14 & UC3 — Author: 524H0031)
INSERT INTO menu_items (item_id, brand_id, item_name_vi, item_name_en, description, unit_price, station_type, status, is_available) VALUES
('PHO-01', 'BR-01', 'Phở Bò Đặc Biệt', 'Special Wagyu Beef Pho', '24-hour bone broth with sliced beef brisket and herbs', 85000.00, 'Wok', 'Active', TRUE),
('BM-02',  'BR-02', 'Chả Giò Hải Sản Giòn', 'Crispy Seafood Spring Rolls', 'Golden fried shrimp and crab spring rolls (4 pcs)', 45000.00, 'Fryer', 'Active', TRUE),
('SLD-01', 'BR-03', 'Salad Ức Gà Bơ Tươi', 'Avocado Grilled Chicken Salad', 'Organic greens with sesame dressing and avocado', 65000.00, 'Assembly', 'Active', TRUE),
('TEA-01', 'BR-03', 'Trà Đào Cam Sả', 'Peach Lemongrass Iced Tea', 'Fresh brewed oolong tea with peach slices and lemongrass', 35000.00, 'Beverage', 'Active', TRUE),
('PHO-99', 'BR-01', 'Phở Gà Lá Chanh (Ngừng bán)', 'Lime Leaf Chicken Pho', 'Seasonal dish retired from catalog', 75000.00, 'Wok', 'Discontinued', FALSE);

-- 6. Customers: LocalCustomer & ForeignTourist (UC1 & UC3)
INSERT INTO customers (customer_id, full_name, phone_number, email_address, customer_type) VALUES
('CUS-01', 'Nguyen Minh Anh', '+84901234567', 'minhanh.nguyen@gmail.com', 'Local'),
('CUS-02', 'John Miller', NULL, 'john.miller@example.com', 'Foreign');

INSERT INTO local_customers (customer_id, phone_number) VALUES
('CUS-01', '+84901234567');

INSERT INTO foreign_tourists (customer_id, passport_number, email_address, preferred_language) VALUES
('CUS-02', 'US8942105', 'john.miller@example.com', 'en');

-- 7. Promotional Vouchers (UC15 & UC3)
INSERT INTO vouchers (voucher_code, discount_percent, max_discount_amount, min_order_amount, start_date, end_date, usage_quota, used_count, status) VALUES
('SBWELCOME10', 10.00, 50000.00, 100000.00, '2026-11-01 00:00:00', '2026-12-31 23:59:59', 200, 12, 'Active'),
('TOURIST20',   20.00, 40000.00, 150000.00, '2026-11-01 00:00:00', '2026-12-31 23:59:59', 100, 8,  'Active');

-- 8. Shippers (UC10)
INSERT INTO shippers (shipper_id, full_name, phone_number, vehicle_plate, current_status, wallet_balance) VALUES
('SHP-01', 'Tran Van Binh', '+84912345678', '59-X1 123.45', 'AVAILABLE', 450000.00);

-- 9. Orders (UC3, UC7, UC10 — Author: 524H0031)
-- ORD-001: Multi-brand order at H01 (distance 3.2 km <= 7.0 km -> fee = 15,000 + 2*5,000 = 25,000 VND; subtotal = 165,000 VND;
--          Quiet-Kitchen 10% = 16,500 VND + Voucher SBWELCOME10 10% = 16,500 VND -> total discount = 33,000 VND; final_total = 157,000 VND)
INSERT INTO orders (order_id, customer_id, hub_id, voucher_code, order_date_time, order_status, delivery_address, is_address_locked, distance_km, subtotal, delivery_fee, discount_amount, final_total, payment_method) VALUES
('ORD-001', 'CUS-01', 'H01', 'SBWELCOME10', '2026-11-28 11:30:00', 'Placed', '45 Le Loi, District 1, HCMC', FALSE, 3.20, 165000.00, 25000.00, 33000.00, 157000.00, 'Online Payment'),
('ORD-002', 'CUS-02', 'H01', NULL,          '2026-11-28 11:35:00', 'Placed', 'Rex Hotel, 141 Nguyen Hue, District 1, HCMC', FALSE, 1.50, 150000.00, 15000.00, 15000.00, 150000.00, 'Cash on Delivery');

-- 10. Order Lines (UC3 — Multi-brand dishes in a single basket)
INSERT INTO order_lines (order_line_id, order_id, item_id, quantity, item_price, line_total, special_notes) VALUES
('OL-001', 'ORD-001', 'PHO-01', 1, 85000.00, 85000.00, 'Extra basil, no chili'),
('OL-002', 'ORD-001', 'BM-02',  1, 45000.00, 45000.00, 'Pack dipping sauce separately'),
('OL-003', 'ORD-001', 'TEA-01', 1, 35000.00, 35000.00, 'Less ice'),
('OL-004', 'ORD-002', 'PHO-01', 1, 85000.00, 85000.00, 'Room 502 delivery'),
('OL-005', 'ORD-002', 'SLD-01', 1, 65000.00, 65000.00, 'Dressing on the side');

-- 11. Kitchen Tickets (UC3 & UC7 — Dispatched per preparation station)
INSERT INTO kitchen_tickets (ticket_id, order_id, station_id, station_type, status) VALUES
('KT-001', 'ORD-001', 'ST-H01-WOK', 'Wok', 'Queued'),
('KT-002', 'ORD-001', 'ST-H01-FRY', 'Fryer', 'Queued'),
('KT-003', 'ORD-001', 'ST-H01-BEV', 'Beverage', 'Queued');

-- 12. Payments (UC3 & UC10 — Paid Online vs Unpaid COD in VND)
INSERT INTO payments (payment_id, order_id, payment_method, payment_amount, payment_status, authorization_code) VALUES
('PAY-001', 'ORD-001', 'Online Payment',   157000.00, 'Paid',   'AUTH-20261128-8841'),
('PAY-002', 'ORD-002', 'Cash on Delivery', 150000.00, 'Unpaid', NULL);

-- 13. Delivery Tasks (UC10)
INSERT INTO delivery_tasks (task_id, order_id, shipper_id, delivery_status, cash_collected) VALUES
('DT-001', 'ORD-002', 'SHP-01', 'Assigned', 0.00);

-- 14. Management Reports (UC16)
INSERT INTO management_reports (report_id, hub_id, report_type, start_date, end_date, total_revenue, total_orders, avg_delivery_minutes, waste_cost) VALUES
('RPT-202611-H01', 'H01', 'Weekly_Sales_Workload_And_SLA', '2026-11-21', '2026-11-28', 18450000.00, 118, 24.50, 320000.00);

-- 15. Audit Logs (NFR5)
INSERT INTO audit_logs (action_name, entity_name, entity_id, performed_by, details) VALUES
('CATALOG_PUBLISHED', 'MenuItem', 'PHO-01', '524H0031 (Administrator)', 'Published bilingual menu item PHO-01 in state Active at H01, H02.'),
('ORDER_PLACED',      'Order',    'ORD-001', '524H0031 (Customer CUS-01)', 'Created multi-brand order ORD-001 in state Placed with 3 station tickets.');
