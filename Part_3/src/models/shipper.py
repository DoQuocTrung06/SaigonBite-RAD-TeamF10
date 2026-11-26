"""
Shipper Entity Model
Author: Nguyen Quang Tuu (524H0136)
Course: RAD Sem01_2627 - SaigonBite Platform
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Shipper:
    shipper_id: str
    full_name: str
    phone_number: str
    vehicle_plate: str
    current_lat: float
    current_lng: float
    wallet_balance: float = 0.0
    is_active: bool = True
    created_at: Optional[datetime] = None

    def update_location(self, lat: float, lng: float):
        """Update current GPS coordinates of the shipper."""
        self.current_lat = lat
        self.current_lng = lng

    def credit_wallet(self, amount: float):
        """Credit delivery fee / earnings to shipper wallet."""
        if amount > 0:
            self.wallet_balance += amount

    def debit_wallet(self, amount: float):
        """Debit COD cash remittance from shipper wallet."""
        self.wallet_balance -= amount

    def to_dict(self):
        return {
            "shipper_id": self.shipper_id,
            "full_name": self.full_name,
            "phone_number": self.phone_number,
            "vehicle_plate": self.vehicle_plate,
            "current_lat": self.current_lat,
            "current_lng": self.current_lng,
            "wallet_balance": self.wallet_balance,
            "is_active": self.is_active,
        }
