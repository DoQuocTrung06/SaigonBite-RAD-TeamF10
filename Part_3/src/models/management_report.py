"""
ManagementReport Entity Model (UC16 Produce management reports)
Author: Nguyen Quang Tuu (524H0136)
Course: RAD Sem01_2627 - SaigonBite Platform
Aligned with Part 2 Final DCD Table 27 (Figure 3.20)
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional


@dataclass
class ManagementReport:
    report_id: str
    report_type: str = "Monthly_Revenue_And_Delivery_Performance"
    hub_id: str = "HUB_01"
    generated_at: datetime = field(default_factory=datetime.now)
    date_from: str = ""
    date_to: str = ""
    start_date: str = ""
    end_date: str = ""
    total_revenue: float = 0.0
    total_orders: int = 0
    delivered_orders: int = 0
    failed_orders: int = 0
    avg_delivery_minutes: float = 24.5
    waste_cost: float = 0.0
    gross_sales_vnd: float = 0.0
    generated_by: str = "Manager"
    metrics_summary: Dict[str, Any] = field(default_factory=dict)
    brand_revenue_breakdown: List[Dict[str, Any]] = field(default_factory=list)
    shipper_sla_breakdown: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self):
        if not self.date_from and self.start_date:
            self.date_from = self.start_date
        if not self.date_to and self.end_date:
            self.date_to = self.end_date
        if not self.start_date and self.date_from:
            self.start_date = self.date_from
        if not self.end_date and self.date_to:
            self.end_date = self.date_to
        if not self.total_revenue and self.gross_sales_vnd:
            self.total_revenue = self.gross_sales_vnd
        if not self.gross_sales_vnd and self.total_revenue:
            self.gross_sales_vnd = self.total_revenue

    # DCD Official Method 1
    def calculateKPIs(self, orders: list, tasks: list):
        """Official DCD Table 27 method: computes report metrics."""
        self.total_orders = len(orders)
        self.delivered_orders = sum(1 for o in orders if getattr(o, "order_status", "") == "Delivered")
        self.failed_orders = sum(1 for o in orders if getattr(o, "order_status", "") == "Delivery_Failed")
        self.total_revenue = sum(getattr(o, "final_amount", 0.0) for o in orders if getattr(o, "order_status", "") == "Delivered")
        self.gross_sales_vnd = self.total_revenue

    # DCD Official Method 2
    def getSummarySnapshot(self) -> Dict[str, Any]:
        """Official DCD Table 27 method: returns summary snapshot."""
        return {
            "reportId": self.report_id,
            "hubId": self.hub_id,
            "totalRevenue": self.total_revenue,
            "totalOrders": self.total_orders,
            "deliveredOrders": self.delivered_orders,
            "failedOrders": self.failed_orders
        }

    def to_summary_text(self) -> str:
        lines = [
            f"=== SAIGONBITE MANAGEMENT REPORT [{self.report_id}] ===",
            f"Type: {self.report_type} | Generated: {self.generated_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Period: {self.date_from} to {self.date_to}",
            f"Total Gross Revenue: {self.total_revenue:,.0f} VND",
            f"Total Orders: {self.total_orders} (Delivered: {self.delivered_orders}, Failed: {self.failed_orders})",
            f"Avg Delivery Time: {self.avg_delivery_minutes:.1f} mins",
            f"SLA Compliance Rate: {(self.delivered_orders / self.total_orders * 100.0) if self.total_orders > 0 else 100.0:.1f}%",
            "-------------------------------------------------------"
        ]
        return "\n".join(lines)
