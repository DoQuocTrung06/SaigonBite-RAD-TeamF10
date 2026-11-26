"""
AuditLogDAO (Data Access Object for Audit Logging - NFR5 Security & Compliance)
Author: Team F10 - SaigonBite Platform
Course: RAD Sem01_2627 - SaigonBite Platform
Aligned with Part 2 Final DCD Tables 19, 20, 25, 27
"""
from typing import Optional
from datetime import datetime
from src.data_access.db_connection import DatabaseConnection


class AuditLogDAO:
    def __init__(self, db_conn: Optional[DatabaseConnection] = None):
        self.db = db_conn or DatabaseConnection.get_instance()

    def recordAuditEntry(self, entity_id: str, actor: str, action: str, details: str = "") -> bool:
        """Appends an immutable audit log entry."""
        conn = self.db.get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO audit_logs (action_name, entity_name, entity_id, performed_by, details, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            action,
            "Order/Delivery",
            entity_id,
            actor,
            details,
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()
        return True
