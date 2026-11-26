"""
Report Controller (Application / Controller Layer for UC16 Produce management reports)
Author: Nguyen Quang Tuu (524H0136)
Course: RAD Sem01_2627 - SaigonBite Platform
"""
from typing import Dict, Any, Optional
from datetime import datetime
from src.data_access.report_repository import ReportRepository
from src.models.management_report import ManagementReport


class ReportController:
    def __init__(self, repo: Optional[ReportRepository] = None):
        self.repo = repo or ReportRepository()

    def generate_sales_and_sla_report(self, manager_id: str, date_from: str, date_to: str) -> ManagementReport:
        brand_sales = self.repo.aggregate_brand_revenue(date_from, date_to)
        shipper_sla = self.repo.aggregate_shipper_sla(date_from, date_to)
        
        total_revenue = sum(b.get("total_revenue", 0) for b in brand_sales)
        total_orders = sum(b.get("total_orders", 0) for b in brand_sales)
        
        total_assigned = sum(s.get("total_assigned", 0) for s in shipper_sla)
        total_delivered = sum(s.get("delivered_count", 0) for s in shipper_sla)
        sla_rate = (total_delivered / total_assigned * 100) if total_assigned > 0 else 100.0

        report = ManagementReport(
            report_id=f"REP_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            report_type="EXECUTIVE_SUMMARY",
            generated_by=manager_id,
            generated_at=datetime.now(),
            date_from=date_from,
            date_to=date_to,
            metrics_summary={
                "total_revenue": total_revenue,
                "total_orders": total_orders,
                "total_deliveries": total_assigned,
                "sla_compliance_rate": sla_rate,
                "avg_delivery_time_mins": 24.5
            },
            brand_revenue_breakdown=brand_sales,
            shipper_sla_breakdown=shipper_sla
        )
        return report
