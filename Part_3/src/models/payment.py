"""
Payment Domain Model (UC10 & UC3)
Author: Nguyen Quang Tuu (524H0136)
Course: RAD Sem01_2627 - SaigonBite Platform
Aligned with Part 2 Final DCD Table 25 (Figure 3.16)
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Payment:
    payment_id: str
    order_id: str
    payment_method: str      # 'COD', 'Card', 'ZaloPay', 'MoMo'
    payment_amount: float
    payment_status: str      # 'PENDING', 'SUCCESS', 'FAILED', 'REFUNDED'
    transaction_ref: Optional[str] = None
    paid_at: Optional[datetime] = None

    def confirmCODPayment(self, collected_amount: float) -> bool:
        """Confirms cash collected upon doorstep food handover."""
        if collected_amount < self.payment_amount:
            raise ValueError(
                f"Insufficient COD cash: expected {self.payment_amount:,.0f} VND, got {collected_amount:,.0f} VND"
            )
        self.payment_status = "SUCCESS"
        self.paid_at = datetime.now()
        return True
