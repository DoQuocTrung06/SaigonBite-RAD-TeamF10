"""
ManagementReport Entity Model (UC16 Produce management reports)
Author: Nguyen Quang Tuu (524H0136)
Course: RAD Sem01_2627 - SaigonBite Platform
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any


@dataclass
class ManagementReport:
    report_id: str
    report_type: str     # 'DAILY_REVENUE', 'BRAND_SALES', 'SHIPPER_SLA', 'KITCHEN_UTILIZATION'
    generated_by: str    # Staff / Manager ID
    generated_at: datetime
    date_from: str
    date_to: str
    metrics_summary: Dict[str, Any] = field(default_factory=dict)
    brand_revenue_breakdown: List[Dict[str, Any]] = field(default_factory=list)
    shipper_sla_breakdown: List[Dict[str, Any]] = field(default_factory=list)

    def to_summary_text(self) -> str:
        lines = [
            f"=== SAIGONBITE MANAGEMENT REPORT [{self.report_id}] ===",
            f"Type: {self.report_type} | Generated: {self.generated_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Period: {self.date_from} to {self.date_to}",
            f"Total Gross Revenue: {self.metrics_summary.get('total_revenue', 0):,.0f} VND",
            f"Total Orders: {self.metrics_summary.get('total_orders', 0)}",
            f"Avg Delivery Time: {self.metrics_summary.get('avg_delivery_time_mins', 0):.1f} mins",
            f"SLA Compliance Rate: {self.metrics_summary.get('sla_compliance_rate', 0):.1f}%",
            "-------------------------------------------------------"
        ]
        return "\n".join(lines)
