"""
Report Repository (Data Access Layer for UC16)
Author: Nguyen Quang Tuu (524H0136)
Course: RAD Sem01_2627 - SaigonBite Platform
"""
from typing import Dict, List, Any
import json
from datetime import datetime
from src.data_access.db_connection import DatabaseConnection


class ReportRepository:
    def __init__(self, db_conn=None):
        self.db = db_conn or DatabaseConnection.get_instance()

    def aggregate_brand_revenue(self, date_from: str, date_to: str) -> List[Dict[str, Any]]:
        conn = self.db.get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT brand_id, brand_name, 
                   COUNT(order_id) as total_orders,
                   SUM(sale_amount) as total_revenue
            FROM brand_sales
            WHERE sale_date BETWEEN ? AND ?
            GROUP BY brand_id, brand_name
            ORDER BY total_revenue DESC
        """, (date_from, date_to))
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def aggregate_shipper_sla(self, date_from: str, date_to: str) -> List[Dict[str, Any]]:
        conn = self.db.get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.shipper_id, s.full_name,
                   COUNT(t.task_id) as total_assigned,
                   SUM(CASE WHEN t.task_status = 'Delivered' THEN 1 ELSE 0 END) as delivered_count,
                   SUM(CASE WHEN t.task_status = 'Failed_Returned' THEN 1 ELSE 0 END) as failed_count,
                   SUM(t.cod_collected_vnd) as total_cod_collected
            FROM shippers s
            LEFT JOIN delivery_tasks t ON s.shipper_id = t.shipper_id
            WHERE t.assigned_at BETWEEN ? AND ?
            GROUP BY s.shipper_id, s.full_name
        """, (date_from, date_to))
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]
