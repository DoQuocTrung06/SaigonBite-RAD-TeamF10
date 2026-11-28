-- ==============================================================================
-- SAIGONBITE CLOUD KITCHEN MULTI-BRAND DELIVERY HUB (OFDH)
-- Relational Database Schema (DDL) for Part 3 Implementation (Section 4.3.1 & 4.3.4)
-- Aligned 100% with Part 2 BRS/SRS Report (Domain Model & Final DCDs UC15, UC7, UC3, UC14, UC10, UC16)
-- Authors: 524H0132, 524H0031, 524H0136
-- ==============================================================================

-- i. Create database
CREATE DATABASE IF NOT EXISTS saigonbite_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE saigonbite_db;

-- ii. Create tables

-- 1. Cloud Kitchen Hubs (UC13, UC14, UC3, UC7, UC16)
CREATE TABLE IF NOT EXISTS hubs (
    hub_id VARCHAR(20) PRIMARY KEY,
    hub_name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    max_capacity_orders INT NOT NULL DEFAULT 50 CHECK (max_capacity_orders > 0),
    hub_status VARCHAR(20) NOT NULL DEFAULT 'Open', -- 'Open', 'Busy', 'Closed'
    is_busy BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Specialized Kitchen Stations within a Hub (Composition: Hub *-- KitchenStation) (UC14, UC7, UC3)
CREATE TABLE IF NOT EXISTS kitchen_stations (
    station_id VARCHAR(20) PRIMARY KEY,
    hub_id VARCHAR(20) NOT NULL,
    station_name VARCHAR(100) NOT NULL,
    station_type VARCHAR(50) NOT NULL CHECK (station_type IN ('Wok', 'Fryer', 'Assembly', 'Beverage', 'Grill', 'Drink_Dessert')),
    current_load_orders INT NOT NULL DEFAULT 0 CHECK (current_load_orders >= 0),
    capacity_limit INT NOT NULL DEFAULT 15 CHECK (capacity_limit > 0),
    FOREIGN KEY (hub_id) REFERENCES hubs(hub_id) ON DELETE CASCADE
);

-- 3. Virtual Restaurant Brands (UC14 — Author: 524H0031)
CREATE TABLE IF NOT EXISTS brands (
    brand_id VARCHAR(20) PRIMARY KEY,
    brand_name VARCHAR(100) UNIQUE NOT NULL,
    cuisine_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Active' -- 'Active', 'Archived'
);

-- 4. Brand-to-Hub Operational Assignments (UC14 — Author: 524H0031)
CREATE TABLE IF NOT EXISTS brand_hubs (
    brand_id VARCHAR(20) NOT NULL,
    hub_id VARCHAR(20) NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (brand_id, hub_id),
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id) ON DELETE CASCADE,
    FOREIGN KEY (hub_id) REFERENCES hubs(hub_id) ON DELETE CASCADE
);

-- 5. Bilingual Menu Items (UC14, UC3 — Author: 524H0031)
CREATE TABLE IF NOT EXISTS menu_items (
    item_id VARCHAR(20) PRIMARY KEY,
    brand_id VARCHAR(20) NOT NULL,
    item_name_vi VARCHAR(150) NOT NULL,
    item_name_en VARCHAR(150) NOT NULL,
    description TEXT,
    unit_price DECIMAL(12, 2) NOT NULL CHECK (unit_price > 0),
    station_type VARCHAR(50) NOT NULL CHECK (station_type IN ('Wok', 'Fryer', 'Assembly', 'Beverage', 'Grill', 'Drink_Dessert')),
    status VARCHAR(20) NOT NULL DEFAULT 'Active' CHECK (status IN ('Active', 'Suspended', 'Discontinued')),
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id) ON DELETE CASCADE
);

-- 6. Customer Supertype & Subtypes (Generalization: Customer <|-- LocalCustomer, ForeignTourist) (UC1, UC3)
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20),
    email_address VARCHAR(100),
    customer_type VARCHAR(20) NOT NULL CHECK (customer_type IN ('Local', 'Foreign')),
    date_registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS local_customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS foreign_tourists (
    customer_id VARCHAR(20) PRIMARY KEY,
    passport_number VARCHAR(30) UNIQUE NOT NULL,
    email_address VARCHAR(100) NOT NULL,
    preferred_language VARCHAR(10) DEFAULT 'en',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- 7. Promotional Vouchers (UC15, UC3 — Authors: 524H0132, 524H0031)
CREATE TABLE IF NOT EXISTS vouchers (
    voucher_code VARCHAR(30) PRIMARY KEY,
    discount_percent DECIMAL(5, 2) NOT NULL DEFAULT 0.00 CHECK (discount_percent >= 0 AND discount_percent <= 50),
    max_discount_amount DECIMAL(12, 2) NOT NULL DEFAULT 0.00 CHECK (max_discount_amount >= 0),
    min_order_amount DECIMAL(12, 2) NOT NULL DEFAULT 0.00 CHECK (min_order_amount >= 0),
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    usage_quota INT NOT NULL DEFAULT 100 CHECK (usage_quota >= 0),
    used_count INT NOT NULL DEFAULT 0 CHECK (used_count >= 0),
    status VARCHAR(20) NOT NULL DEFAULT 'Active' -- 'Scheduled', 'Active', 'Expired', 'Deactivated'
);

-- 8. Delivery Couriers / Shippers (UC10 — Author: 524H0136)
CREATE TABLE IF NOT EXISTS shippers (
    shipper_id VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    vehicle_plate VARCHAR(20) NOT NULL,
    current_status VARCHAR(20) NOT NULL DEFAULT 'AVAILABLE',
    wallet_balance DECIMAL(12, 2) NOT NULL DEFAULT 0.00
);

-- 9. Customer Orders (UC3, UC7, UC10, UC16 — Authors: 524H0031, 524H0132, 524H0136)
CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    hub_id VARCHAR(20) NOT NULL,
    voucher_code VARCHAR(30),
    order_date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    order_status VARCHAR(30) NOT NULL DEFAULT 'Placed'
        CHECK (order_status IN ('Placed', 'Pending_Kitchen', 'Confirmed', 'Preparing', 'Ready', 'Delivering', 'Delivered', 'Cancelled', 'Failed')),
    delivery_address VARCHAR(255) NOT NULL,
    is_address_locked BOOLEAN NOT NULL DEFAULT FALSE,
    distance_km DECIMAL(6, 2) NOT NULL CHECK (distance_km > 0 AND distance_km <= 7.0),
    subtotal DECIMAL(12, 2) NOT NULL CHECK (subtotal >= 0),
    delivery_fee DECIMAL(12, 2) NOT NULL CHECK (delivery_fee >= 15000),
    discount_amount DECIMAL(12, 2) NOT NULL DEFAULT 0.00 CHECK (discount_amount >= 0),
    final_total DECIMAL(12, 2) NOT NULL CHECK (final_total >= 0),
    payment_method VARCHAR(30) NOT NULL, -- 'Cash on Delivery', 'Online Payment'
    rejection_reason VARCHAR(255),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (hub_id) REFERENCES hubs(hub_id),
    FOREIGN KEY (voucher_code) REFERENCES vouchers(voucher_code)
);

-- 10. Order Line Items (Association Class: Order 1..* OrderLine *..1 MenuItem) (UC3 — Author: 524H0031)
CREATE TABLE IF NOT EXISTS order_lines (
    order_line_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL,
    item_id VARCHAR(20) NOT NULL,
    quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    item_price DECIMAL(12, 2) NOT NULL CHECK (item_price > 0),
    line_total DECIMAL(12, 2) NOT NULL CHECK (line_total > 0),
    special_notes VARCHAR(255),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
);

-- 11. Kitchen Preparation Station Tickets (UC3, UC7 — Authors: 524H0031, 524H0132)
CREATE TABLE IF NOT EXISTS kitchen_tickets (
    ticket_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL,
    station_id VARCHAR(20) NOT NULL,
    station_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Queued', -- 'Queued', 'Preparing', 'Completed', 'Cancelled'
    printed_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_time TIMESTAMP NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (station_id) REFERENCES kitchen_stations(station_id)
);

-- 12. Order Payments (UC3, UC10 — Authors: 524H0031, 524H0136)
CREATE TABLE IF NOT EXISTS payments (
    payment_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL UNIQUE,
    payment_method VARCHAR(30) NOT NULL,
    payment_amount DECIMAL(12, 2) NOT NULL CHECK (payment_amount >= 0),
    payment_status VARCHAR(20) NOT NULL DEFAULT 'Unpaid', -- 'Paid', 'Unpaid', 'Refunded'
    authorization_code VARCHAR(100),
    payment_date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
);

-- 13. Last-Mile Delivery Tasks (UC10 — Author: 524H0136)
CREATE TABLE IF NOT EXISTS delivery_tasks (
    task_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL UNIQUE,
    shipper_id VARCHAR(20) NOT NULL,
    delivery_status VARCHAR(30) NOT NULL DEFAULT 'Assigned', -- 'Assigned', 'PickedUp', 'Delivered', 'Failed'
    pickup_time TIMESTAMP NULL,
    delivered_time TIMESTAMP NULL,
    cash_collected DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    failure_reason VARCHAR(255),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (shipper_id) REFERENCES shippers(shipper_id)
);

-- 14. Operational Management Reports (UC16 — Author: 524H0136)
CREATE TABLE IF NOT EXISTS management_reports (
    report_id VARCHAR(20) PRIMARY KEY,
    hub_id VARCHAR(20) NOT NULL,
    report_type VARCHAR(50) NOT NULL,
    generated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_revenue DECIMAL(14, 2) NOT NULL DEFAULT 0.00,
    total_orders INT NOT NULL DEFAULT 0,
    avg_delivery_minutes DECIMAL(6, 2) NOT NULL DEFAULT 0.00,
    waste_cost DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    FOREIGN KEY (hub_id) REFERENCES hubs(hub_id)
);

-- 15. Immutable Security & State Audit Logs (NFR5 — All Use Cases)
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    action_name VARCHAR(100) NOT NULL,
    entity_name VARCHAR(50) NOT NULL,
    entity_id VARCHAR(50) NOT NULL,
    performed_by VARCHAR(50) NOT NULL,
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
