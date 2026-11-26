"""
Delivery Repository (Data Access Layer for UC10)
Author: Nguyen Quang Tuu (524H0136)
Course: RAD Sem01_2627 - SaigonBite Platform
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from src.data_access.db_connection import DatabaseConnection
from src.models.delivery_task import DeliveryTask
from src.models.order import Order
from src.models.shipper import Shipper


class DeliveryRepository:
    def __init__(self, db_conn: Optional[DatabaseConnection] = None):
        self.db = db_conn or DatabaseConnection.get_instance()

    def get_task_by_id(self, task_id: str) -> Optional[DeliveryTask]:
        conn = self.db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM delivery_tasks WHERE task_id = ?", (task_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        return DeliveryTask(
            task_id=row["task_id"],
            order_id=row["order_id"],
            shipper_id=row["shipper_id"],
            qr_code_token=row["qr_code_token"],
            task_status=row["task_status"],
            assigned_at=datetime.fromisoformat(row["assigned_at"]),
            picked_up_at=datetime.fromisoformat(row["picked_up_at"]) if row["picked_up_at"] else None,
            arrived_dropoff_at=datetime.fromisoformat(row["arrived_dropoff_at"]) if row["arrived_dropoff_at"] else None,
            wait_start_time=datetime.fromisoformat(row["wait_start_time"]) if row["wait_start_time"] else None,
            completed_at=datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None,
            cod_collected_vnd=row["cod_collected_vnd"],
            failure_reason=row["failure_reason"]
        )

    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        conn = self.db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        return Order(
            order_id=row["order_id"],
            customer_id=row["customer_id"],
            hub_id=row["hub_id"],
            delivery_address=row["delivery_address"],
            distance_km=row["distance_km"],
            total_amount=row["total_amount"],
            delivery_fee=row["delivery_fee"],
            discount_amount=row["discount_amount"],
            final_amount=row["final_amount"],
            payment_method=row["payment_method"],
            order_status=row["order_status"],
            created_at=datetime.fromisoformat(row["created_at"]),
            confirmed_at=datetime.fromisoformat(row["confirmed_at"]) if row["confirmed_at"] else None,
            ready_at=datetime.fromisoformat(row["ready_at"]) if row["ready_at"] else None,
            delivered_at=datetime.fromisoformat(row["delivered_at"]) if row["delivered_at"] else None,
            cancellation_reason=row["cancellation_reason"]
        )

    def get_shipper_by_id(self, shipper_id: str) -> Optional[Shipper]:
        conn = self.db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM shippers WHERE shipper_id = ?", (shipper_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        return Shipper(
            shipper_id=row["shipper_id"],
            full_name=row["full_name"],
            phone_number=row["phone_number"],
            vehicle_plate=row["vehicle_plate"],
            current_lat=row["current_lat"],
            current_lng=row["current_lng"],
            wallet_balance=row["wallet_balance"],
            is_active=bool(row["is_active"])
        )

    def save_task(self, task: DeliveryTask):
        conn = self.db.get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO delivery_tasks (
                task_id, order_id, shipper_id, qr_code_token, task_status,
                assigned_at, picked_up_at, arrived_dropoff_at, wait_start_time,
                completed_at, cod_collected_vnd, failure_reason
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task.task_id, task.order_id, task.shipper_id, task.qr_code_token, task.task_status,
            task.assigned_at.isoformat() if task.assigned_at else None,
            task.picked_up_at.isoformat() if task.picked_up_at else None,
            task.arrived_dropoff_at.isoformat() if task.arrived_dropoff_at else None,
            task.wait_start_time.isoformat() if task.wait_start_time else None,
            task.completed_at.isoformat() if task.completed_at else None,
            task.cod_collected_vnd, task.failure_reason
        ))
        conn.commit()
        conn.close()

    def update_order_status(self, order_id: str, new_status: str, failure_reason: Optional[str] = None):
        conn = self.db.get_connection()
        cur = conn.cursor()
        delivered_at = datetime.now().isoformat() if new_status == "Delivered" else None
        cur.execute("""
            UPDATE orders 
            SET order_status = ?, delivered_at = COALESCE(?, delivered_at), cancellation_reason = ?
            WHERE order_id = ?
        """, (new_status, delivered_at, failure_reason, order_id))
        conn.commit()
        conn.close()

    def update_shipper_wallet(self, shipper_id: str, amount_delta: float):
        conn = self.db.get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE shippers 
            SET wallet_balance = wallet_balance + ? 
            WHERE shipper_id = ?
        """, (amount_delta, shipper_id))
        conn.commit()
        conn.close()
