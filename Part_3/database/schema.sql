-- ==============================================================================
-- SAIGONBITE CLOUD KITCHEN MULTI-BRAND DELIVERY HUB
-- Relational Database Schema (DDL) for Part 3 Implementation
-- Aligned 100% with Part 2 BRS/SRS Report (Section 2.1.7, Domain Model, Tables 19-28)
-- ==============================================================================

-- 0. Create and select database
CREATE DATABASE IF NOT EXISTS saigonbite_db;
USE saigonbite_db;

-- 1. ENUMS / TYPES (or CHECK constraints)
-- Supported Customer Types: LocalCustomer, ForeignTourist (Feedback Log A-04)

CREATE TABLE IF NOT EXISTS hubs (
    hub_id VARCHAR(20) PRIMARY KEY,
    hub_name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    max_capacity_orders INT NOT NULL DEFAULT 50,
    is_busy BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS kitchen_stations (
    station_id VARCHAR(20) PRIMARY KEY,
    hub_id VARCHAR(20) NOT NULL,
    station_name VARCHAR(100) NOT NULL,
    station_type VARCHAR(50) NOT NULL, -- 'Grill', 'Drink_Dessert', 'Fryer', 'Packaging'
    current_load_orders INT NOT NULL DEFAULT 0,
    capacity_limit INT NOT NULL DEFAULT 15,
    FOREIGN KEY (hub_id) REFERENCES hubs(hub_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS brands (
    brand_id VARCHAR(20) PRIMARY KEY,
    brand_name VARCHAR(100) NOT NULL,
    cuisine_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS menu_items (
    item_id VARCHAR(20) PRIMARY KEY,
    brand_id VARCHAR(20) NOT NULL,
    item_name VARCHAR(150) NOT NULL,
    description TEXT,
    unit_price DECIMAL(12, 2) NOT NULL CHECK (unit_price > 0),
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    station_type VARCHAR(50) NOT NULL,
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id) ON DELETE CASCADE
);

-- Master Customer table
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    customer_type VARCHAR(20) NOT NULL CHECK (customer_type IN ('Local', 'Foreign')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Subtype 1: LocalCustomer (Phone-based authentication per Section 2.1.7)
CREATE TABLE IF NOT EXISTS local_customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- Subtype 2: ForeignTourist (Passport/Email-based authentication per Feedback Log A-04)
CREATE TABLE IF NOT EXISTS foreign_tourists (
    customer_id VARCHAR(20) PRIMARY KEY,
    passport_number VARCHAR(30) UNIQUE NOT NULL,
    email_address VARCHAR(100) NOT NULL,
    preferred_language VARCHAR(10) DEFAULT 'en',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS vouchers (
    voucher_code VARCHAR(30) PRIMARY KEY,
    discount_percent DECIMAL(5, 2) NOT NULL DEFAULT 0.00 CHECK (discount_percent >= 0 AND discount_percent <= 100),
    max_discount_amount DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    min_order_amount DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    usage_limit INT NOT NULL DEFAULT 100,
    used_count INT NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS shippers (
    shipper_id VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    vehicle_plate VARCHAR(20) NOT NULL,
    current_status VARCHAR(20) NOT NULL DEFAULT 'AVAILABLE', -- 'AVAILABLE', 'DELIVERING', 'OFFLINE'
    wallet_balance DECIMAL(12, 2) NOT NULL DEFAULT 0.00
);

CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    hub_id VARCHAR(20) NOT NULL,
    voucher_code VARCHAR(30),
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    order_status VARCHAR(30) NOT NULL DEFAULT 'Pending_Kitchen',
    delivery_address VARCHAR(255) NOT NULL,
    distance_km DECIMAL(6, 2) NOT NULL CHECK (distance_km > 0 AND distance_km <= 7.0),
    subtotal DECIMAL(12, 2) NOT NULL,
    delivery_fee DECIMAL(12, 2) NOT NULL,
    discount_amount DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    final_total DECIMAL(12, 2) NOT NULL,
    payment_method VARCHAR(20) NOT NULL, -- 'COD', 'Card', 'ZaloPay', 'MoMo'
    payment_status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (hub_id) REFERENCES hubs(hub_id),
    FOREIGN KEY (voucher_code) REFERENCES vouchers(voucher_code)
);

CREATE TABLE IF NOT EXISTS order_lines (
    order_line_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL,
    item_id VARCHAR(20) NOT NULL,
    quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    unit_price DECIMAL(12, 2) NOT NULL CHECK (unit_price > 0),
    subtotal DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
);

CREATE TABLE IF NOT EXISTS kitchen_tickets (
    ticket_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL,
    station_id VARCHAR(20) NOT NULL,
    ticket_status VARCHAR(20) NOT NULL DEFAULT 'QUEUED', -- 'QUEUED', 'COOKING', 'READY'
    estimated_cook_time_mins INT NOT NULL DEFAULT 15,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (station_id) REFERENCES kitchen_stations(station_id)
);

CREATE TABLE IF NOT EXISTS delivery_tasks (
    task_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL UNIQUE,
    shipper_id VARCHAR(20) NOT NULL,
    delivery_status VARCHAR(30) NOT NULL DEFAULT 'Assigned', -- 'Assigned', 'Picked_Up', 'Delivered', 'Delivery_Failed'
    cod_amount DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    delivery_fee_earned DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    picked_up_at TIMESTAMP,
    delivered_at TIMESTAMP,
    failed_at TIMESTAMP,
    failure_reason VARCHAR(255),
    proof_image_url VARCHAR(255),
    return_manifest_status VARCHAR(30),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (shipper_id) REFERENCES shippers(shipper_id)
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL UNIQUE,
    payment_method VARCHAR(20) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING', -- 'PENDING', 'SUCCESS', 'FAILED', 'REFUNDED'
    transaction_ref VARCHAR(100),
    paid_at TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE IF NOT EXISTS management_reports (
    report_id VARCHAR(20) PRIMARY KEY,
    hub_id VARCHAR(20) NOT NULL,
    report_period VARCHAR(20) NOT NULL, -- e.g. '2026-11'
    report_type VARCHAR(50) NOT NULL,   -- 'Monthly_Revenue_And_Delivery_Performance'
    total_orders INT NOT NULL DEFAULT 0,
    completed_orders INT NOT NULL DEFAULT 0,
    failed_orders INT NOT NULL DEFAULT 0,
    gross_revenue DECIMAL(14, 2) NOT NULL DEFAULT 0.00,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hub_id) REFERENCES hubs(hub_id)
);

CREATE TABLE IF NOT EXISTS audit_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    action_name VARCHAR(100) NOT NULL,
    entity_name VARCHAR(50) NOT NULL,
    entity_id VARCHAR(50) NOT NULL,
    performed_by VARCHAR(50) NOT NULL,
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
