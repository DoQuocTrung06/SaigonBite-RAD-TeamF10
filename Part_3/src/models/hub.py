"""
Hub Domain Model (UC10, UC16 & UC3)
Author: Nguyen Quang Tuu (524H0136)
Course: RAD Sem01_2627 - SaigonBite Platform
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Hub:
    hub_id: str
    hub_name: str
    address: str
    latitude: float
    longitude: float
    max_capacity_orders: int = 50
    is_busy: bool = False
    active_station_count: int = 4

    def getActiveStationCount(self) -> int:
        """Returns the number of active kitchen stations operating in this Hub."""
        return self.active_station_count
