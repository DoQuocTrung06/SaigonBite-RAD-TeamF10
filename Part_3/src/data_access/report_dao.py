"""
ReportDAO (Data Access Object for Management Reports - UC16)
Author: Nguyen Quang Tuu (524H0136)
Course: RAD Sem01_2627 - SaigonBite Platform
Aligned with Part 2 Final DCD Table 27 (Figure 3.20)
"""
from typing import Optional
from datetime import datetime
from src.data_access.db_connection import DatabaseConnection
from src.models.management_report import ManagementReport


class ReportDAO:
    def __init__(self, db_conn: Optional[DatabaseConnection] = None):
        self.db = db_conn or DatabaseConnection.get_instance()

    def saveReport(self, report: ManagementReport) -> bool:
        """Persists management report snapshot to database."""
        conn = self.db.get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO management_reports (
                report_id, hub_id, report_period, report_type,
                total_orders, completed_orders, failed_orders,
                gross_revenue, generated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            report.report_id,
            "HUB_01",
            f"{report.start_date}_{report.end_date}",
            report.report_type,
            report.total_orders,
            report.delivered_orders,
            report.failed_orders,
            report.gross_sales_vnd,
            report.generated_at.isoformat() if report.generated_at else datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()
        return True

    def findReportById(self, report_id: str) -> Optional[ManagementReport]:
        """Retrieves saved report by reportId."""
        conn = self.db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM management_reports WHERE report_id = ?", (report_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        return ManagementReport(
            report_id=row["report_id"],
            report_type=row["report_type"],
            start_date=row["report_period"].split("_")[0] if "_" in row["report_period"] else "",
            end_date=row["report_period"].split("_")[1] if "_" in row["report_period"] else "",
            total_orders=row["total_orders"],
            delivered_orders=row["completed_orders"],
            failed_orders=row["failed_orders"],
            gross_sales_vnd=row["gross_revenue"]
        )
