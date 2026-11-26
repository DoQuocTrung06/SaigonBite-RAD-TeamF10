"""
DeliveryTask Entity Model (UC10 Deliver an order)
Author: Nguyen Quang Tuu (524H0136)
Course: RAD Sem01_2627 - SaigonBite Platform
Aligned 100% with Part 2 Final DCD Table 25 (Figure 3.16)
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
    proof_photo_url: Optional[str] = None

    # DCD Official Method 1
    def updatePickupStatus(self, timestamp: Optional[datetime] = None):
        """Official DCD Table 25 method: updates pickup timestamp and status."""
        self.task_status = "Picked_Up"
        self.picked_up_at = timestamp or datetime.now()

    # DCD Official Method 2
    def completeDelivery(self, cod_amount: float = 0.0, photo_url: Optional[str] = None):
        """Official DCD Table 25 method: records COD collection and success."""
        self.task_status = "Delivered"
        self.completed_at = datetime.now()
        self.cod_collected_vnd = cod_amount
        self.proof_photo_url = photo_url

    # DCD Official Method 3
    def markFailed(self, reason: str = "Customer unreachable after 10m", photo_url: Optional[str] = None):
        """Official DCD Table 25 method: marks delivery failure and reason."""
        self.task_status = "Failed_Returned"
        self.completed_at = datetime.now()
        self.failure_reason = reason
        self.proof_photo_url = photo_url

    # Backward-compatible helper methods for existing demo scripts
    def scan_qr_and_pickup(self, scanned_token: str) -> bool:
        if self.task_status != "Assigned":
            raise ValueError(f"Task is in {self.task_status} status, cannot pickup")
        if self.qr_code_token != scanned_token:
            raise ValueError("QR code token mismatch! Invalid package.")
        self.updatePickupStatus()
        return True

    def start_delivering(self):
        if self.task_status != "Picked_Up":
            raise ValueError("Must pickup package before delivering")
        self.task_status = "Delivering"

    def arrive_at_dropoff(self):
        self.arrived_dropoff_at = datetime.now()

    def start_10_min_countdown(self):
        self.task_status = "Waiting_Customer_10Min"
        self.wait_start_time = datetime.now()

    def confirm_successful_delivery(self, cod_amount: float = 0.0):
        self.completeDelivery(cod_amount)

    def mark_delivery_failed(self, reason: str = "Customer unreachable after 10m"):
        self.markFailed(reason)
