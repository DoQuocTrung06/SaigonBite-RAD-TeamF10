"""
Database Connection & Initialization Helper
Author: Nguyen Quang Tuu (524H0136)
Course: RAD Sem01_2627 - SaigonBite Platform
"""
import sqlite3
import os
from typing import Optional


class DatabaseConnection:
    _instance: Optional['DatabaseConnection'] = None

    def __init__(self, db_path: str = "saigonbite_dev.db"):
        self.db_path = db_path
        self._init_schema()

    @classmethod
    def get_instance(cls, db_path: str = "saigonbite_dev.db") -> 'DatabaseConnection':
        if cls._instance is None:
            cls._instance = cls(db_path)
        return cls._instance

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _init_schema(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 1. Shippers table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS shippers (
            shipper_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            phone_number TEXT NOT NULL UNIQUE,
            vehicle_plate TEXT NOT NULL,
            current_lat REAL NOT NULL,
            current_lng REAL NOT NULL,
            wallet_balance REAL DEFAULT 0.0 CHECK(wallet_balance >= 0.0),
            is_active INTEGER DEFAULT 1
        );
        """)

        # 2. Orders table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            hub_id TEXT NOT NULL,
            delivery_address TEXT NOT NULL,
            distance_km REAL NOT NULL CHECK(distance_km <= 7.0),
            total_amount REAL NOT NULL CHECK(total_amount > 0),
            delivery_fee REAL NOT NULL CHECK(delivery_fee >= 0),
            discount_amount REAL DEFAULT 0 CHECK(discount_amount >= 0),
            final_amount REAL NOT NULL CHECK(final_amount > 0),
            payment_method TEXT NOT NULL CHECK(payment_method IN ('COD', 'ONLINE_CARD')),
            order_status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            confirmed_at TEXT,
            ready_at TEXT,
            delivered_at TEXT,
            cancellation_reason TEXT
        );
        """)

        # 3. Delivery tasks table (UC10)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS delivery_tasks (
            task_id TEXT PRIMARY KEY,
            order_id TEXT NOT NULL,
            shipper_id TEXT NOT NULL,
            qr_code_token TEXT NOT NULL UNIQUE,
            task_status TEXT NOT NULL,
            assigned_at TEXT NOT NULL,
            picked_up_at TEXT,
            arrived_dropoff_at TEXT,
            wait_start_time TEXT,
            completed_at TEXT,
            cod_collected_vnd REAL DEFAULT 0.0,
            failure_reason TEXT,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (shipper_id) REFERENCES shippers(shipper_id)
        );
        """)

        # 4. Brand sales & management reports (UC16)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS brand_sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand_id TEXT NOT NULL,
            brand_name TEXT NOT NULL,
            order_id TEXT NOT NULL,
            sale_amount REAL NOT NULL,
            sale_date TEXT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS management_reports (
            report_id TEXT PRIMARY KEY,
            report_type TEXT NOT NULL,
            generated_by TEXT NOT NULL,
            generated_at TEXT NOT NULL,
            date_from TEXT NOT NULL,
            date_to TEXT NOT NULL,
            summary_json TEXT NOT NULL
        );
        """)

        conn.commit()
        conn.close()
