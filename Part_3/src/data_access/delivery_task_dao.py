"""
DeliveryTaskDAO (Data Access Object for UC10)
Author: Nguyen Quang Tuu (524H0136)
Course: RAD Sem01_2627 - SaigonBite Platform
Aligned 100% with Part 2 Final DCD Table 25 (Figure 3.16)
"""
from typing import Optional, List
from datetime import datetime
from src.data_access.db_connection import DatabaseConnection
from src.models.delivery_task import DeliveryTask


class DeliveryTaskDAO:
    def __init__(self, db_conn: Optional[DatabaseConnection] = None):
        self.db = db_conn or DatabaseConnection.get_instance()

    def findByOrderId(self, order_id: str) -> Optional[DeliveryTask]:
        """Find delivery task corresponding to an order."""
        conn = self.db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM delivery_tasks WHERE order_id = ?", (order_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        r = dict(row)
        return DeliveryTask(
            task_id=r["task_id"],
            order_id=r["order_id"],
            shipper_id=r["shipper_id"],
            qr_code_token=r.get("qr_code_token", f"QR_SGB_{r['order_id']}"),
            task_status=r["task_status"],
            assigned_at=datetime.fromisoformat(r["assigned_at"]) if r.get("assigned_at") else datetime.now(),
            picked_up_at=datetime.fromisoformat(r["picked_up_at"]) if r.get("picked_up_at") else None,
            arrived_dropoff_at=datetime.fromisoformat(r["arrived_dropoff_at"]) if r.get("arrived_dropoff_at") else None,
            wait_start_time=datetime.fromisoformat(r["wait_start_time"]) if r.get("wait_start_time") else None,
            completed_at=datetime.fromisoformat(r["completed_at"]) if r.get("completed_at") else None,
            cod_collected_vnd=r.get("cod_collected_vnd", 0.0),
            failure_reason=r.get("failure_reason")
        )

    def findById(self, task_id: str) -> Optional[DeliveryTask]:
        """Find delivery task by primary key taskId."""
        conn = self.db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM delivery_tasks WHERE task_id = ?", (task_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        r = dict(row)
        return DeliveryTask(
            task_id=r["task_id"],
            order_id=r["order_id"],
            shipper_id=r["shipper_id"],
            qr_code_token=r.get("qr_code_token", f"QR_SGB_{r['order_id']}"),
            task_status=r["task_status"],
            assigned_at=datetime.fromisoformat(r["assigned_at"]) if r.get("assigned_at") else datetime.now(),
            picked_up_at=datetime.fromisoformat(r["picked_up_at"]) if r.get("picked_up_at") else None,
            arrived_dropoff_at=datetime.fromisoformat(r["arrived_dropoff_at"]) if r.get("arrived_dropoff_at") else None,
            wait_start_time=datetime.fromisoformat(r["wait_start_time"]) if r.get("wait_start_time") else None,
            completed_at=datetime.fromisoformat(r["completed_at"]) if r.get("completed_at") else None,
            cod_collected_vnd=r.get("cod_collected_vnd", 0.0),
            failure_reason=r.get("failure_reason")
        )

    def update(self, task: DeliveryTask) -> bool:
        """Persist modified task state to database."""
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
            task.cod_collected_vnd,
            task.failure_reason
        ))
        conn.commit()
        conn.close()
        return True
