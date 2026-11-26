"""
DeliveryTask Entity Model (UC10 Deliver an order)
Author: Nguyen Quang Tuu (524H0136)
Course: RAD Sem01_2627 - SaigonBite Platform
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class DeliveryTask:
    task_id: str
    order_id: str
    shipper_id: str
    qr_code_token: str
    task_status: str     # 'Assigned', 'Picked_Up', 'Delivering', 'Waiting_Customer_10Min', 'Delivered', 'Failed_Returned'
    assigned_at: datetime
    picked_up_at: Optional[datetime] = None
    arrived_dropoff_at: Optional[datetime] = None
    wait_start_time: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    cod_collected_vnd: float = 0.0
    failure_reason: Optional[str] = None

    def scan_qr_and_pickup(self, scanned_token: str) -> bool:
        """Shipper scans QR code at Hub package station to confirm pickup."""
        if self.task_status != "Assigned":
            raise ValueError(f"Task is in {self.task_status} status, cannot pickup")
        if self.qr_code_token != scanned_token:
            raise ValueError("QR code token mismatch! Invalid package.")
        self.task_status = "Picked_Up"
        self.picked_up_at = datetime.now()
        return True

    def start_delivering(self):
        """Shipper departs Hub and begins navigation to customer."""
        if self.task_status != "Picked_Up":
            raise ValueError("Must pickup package before delivering")
        self.task_status = "Delivering"

    def arrive_at_dropoff(self):
        """Shipper arrives at customer delivery GPS location."""
        self.arrived_dropoff_at = datetime.now()

    def start_10_min_countdown(self):
        """When calling customer has no answer, start 10-minute timeout."""
        self.task_status = "Waiting_Customer_10Min"
        self.wait_start_time = datetime.now()

    def confirm_successful_delivery(self, cod_amount: float = 0.0):
        """Delivery succeeded, record COD collection and timestamp."""
        if self.task_status not in ("Delivering", "Waiting_Customer_10Min", "Picked_Up"):
            raise ValueError(f"Cannot complete delivery from status: {self.task_status}")
        self.task_status = "Delivered"
        self.completed_at = datetime.now()
        self.cod_collected_vnd = cod_amount

    def mark_delivery_failed(self, reason: str = "Customer unreachable after 10m"):
        """Customer failed to show up after 10 minutes timeout."""
        self.task_status = "Failed_Returned"
        self.completed_at = datetime.now()
        self.failure_reason = reason
