"""
OrderDAO (Data Access Object for Orders - shared across UC3, UC7, UC10, UC16)
Author: Team F10 - SaigonBite Platform
Course: RAD Sem01_2627 - SaigonBite Platform
Aligned with Part 2 Final DCD Tables 20, 25, 27
"""
from typing import Optional, List
from datetime import datetime
from src.data_access.db_connection import DatabaseConnection
from src.models.order import Order


class OrderDAO:
    def __init__(self, db_conn: Optional[DatabaseConnection] = None):
        self.db = db_conn or DatabaseConnection.get_instance()

    def findById(self, order_id: str) -> Optional[Order]:
        """Query order by orderId."""
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

    def updateStatus(self, order_id: str, status: str, reason: Optional[str] = None) -> bool:
        """Update order lifecycle status in database."""
        conn = self.db.get_connection()
        cur = conn.cursor()
        now_str = datetime.now().isoformat()
        if status == "Delivered":
            cur.execute(
                "UPDATE orders SET order_status = ?, delivered_at = ? WHERE order_id = ?",
                (status, now_str, order_id)
            )
        elif status == "Delivery_Failed":
            cur.execute(
                "UPDATE orders SET order_status = ?, cancellation_reason = ? WHERE order_id = ?",
                (status, reason or "Delivery timeout", order_id)
            )
        else:
            cur.execute(
                "UPDATE orders SET order_status = ? WHERE order_id = ?",
                (status, order_id)
            )
        conn.commit()
        conn.close()
        return True

    def getOrdersByHubAndDate(self, hub_id: str, start_date: str, end_date: str) -> List[Order]:
        """Query orders for management reporting (UC16)."""
        conn = self.db.get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM orders 
            WHERE hub_id = ? AND date(created_at) BETWEEN date(?) AND date(?)
        """, (hub_id, start_date, end_date))
        rows = cur.fetchall()
        conn.close()
        results = []
        for row in rows:
            results.append(Order(
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
            ))
        return results
