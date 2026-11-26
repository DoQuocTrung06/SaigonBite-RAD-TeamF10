"""
Order Entity Model (Subsystem Perspective)
Author: Nguyen Quang Tuu (524H0136)
Course: RAD Sem01_2627 - SaigonBite Platform
Aligned with Part 2 Final DCD Tables 20, 21, 25, 27
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Order:
    order_id: str
    customer_id: str
    hub_id: str
    delivery_address: str
    distance_km: float
    total_amount: float
    delivery_fee: float
    discount_amount: float
    final_amount: float
    payment_method: str  # 'COD' or 'ONLINE_CARD'
    order_status: str    # 'Created', 'Confirmed', 'Ready_for_Pickup', 'Out_for_Delivery', 'Delivered', 'Delivery_Failed', 'Cancelled'
    created_at: datetime
    confirmed_at: Optional[datetime] = None
    ready_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    cancellation_reason: Optional[str] = None

    # DCD Official Method (Tables 20, 25)
    def updateStatus(self, new_status: str, reason: Optional[str] = None):
        """Official DCD Table 25 method: transitions order status."""
        self.transition_to(new_status, reason)

    def transition_to(self, new_status: str, reason: Optional[str] = None):
        """State transition logic aligned with Order State Machine."""
        valid_transitions = {
            "Created": ["Confirmed", "Cancelled"],
            "Confirmed": ["Ready_for_Pickup", "Cancelled"],
            "Ready_for_Pickup": ["Out_for_Delivery", "Cancelled"],
            "Out_for_Delivery": ["Delivered", "Delivery_Failed"],
            "Delivery_Failed": ["Cancelled"],
            "Delivered": [],
            "Cancelled": []
        }
        if new_status not in valid_transitions.get(self.order_status, []):
            raise ValueError(
                f"Invalid transition from {self.order_status} to {new_status}"
            )
        self.order_status = new_status
        if new_status == "Delivered":
            self.delivered_at = datetime.now()
        elif new_status in ("Cancelled", "Delivery_Failed"):
            self.cancellation_reason = reason
