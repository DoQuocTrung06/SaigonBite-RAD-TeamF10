"""
Customer Domain Model Hierarchy (Section 2.1.7 & Feedback Log A-04)
Author: Team F10 - SaigonBite Platform
Course: RAD Sem01_2627 - SaigonBite Platform
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Customer:
    customer_id: str
    full_name: str
    customer_type: str  # 'Local' or 'Foreign'
    created_at: datetime = datetime.now()


@dataclass
class LocalCustomer(Customer):
    phone_number: str = ""

    def __post_init__(self):
        self.customer_type = "Local"


@dataclass
class ForeignTourist(Customer):
    passport_number: str = ""
    email_address: str = ""
    preferred_language: str = "en"

    def __post_init__(self):
        self.customer_type = "Foreign"
