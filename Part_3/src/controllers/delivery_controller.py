"""
Delivery Controller (Application / Controller Layer for UC10 Deliver an order)
Author: Nguyen Quang Tuu (524H0136)
Course: RAD Sem01_2627 - SaigonBite Platform
"""
from typing import Dict, Any, Optional
from datetime import datetime
from src.data_access.delivery_repository import DeliveryRepository
from src.models.delivery_task import DeliveryTask


class DeliveryController:
    def __init__(self, delivery_repo: Optional[DeliveryRepository] = None):
        self.repo = delivery_repo or DeliveryRepository()

    def scan_package_qr(self, task_id: str, qr_token: str) -> Dict[str, Any]:
        """Actor (Shipper) scans QR code on packed food parcel at Hub."""
        task = self.repo.get_task_by_id(task_id)
        if not task:
            return {"success": False, "message": f"Task {task_id} not found"}
        
        try:
            task.scan_qr_and_pickup(qr_token)
            self.repo.save_task(task)
            # Update order state to Out_for_Delivery
            self.repo.update_order_status(task.order_id, "Out_for_Delivery")
            return {
                "success": True,
                "message": "Package QR verified. Status: Picked Up. Order out for delivery.",
                "order_id": task.order_id,
                "task_status": task.task_status
            }
        except ValueError as e:
            return {"success": False, "message": str(e)}

    def navigate_to_dropoff(self, task_id: str, current_lat: float, current_lng: float) -> Dict[str, Any]:
        """Track GPS progress toward customer address."""
        task = self.repo.get_task_by_id(task_id)
        if not task:
            return {"success": False, "message": "Task not found"}
        
        shipper = self.repo.get_shipper_by_id(task.shipper_id)
        if shipper:
            shipper.update_location(current_lat, current_lng)
        
        task.arrive_at_dropoff()
        self.repo.save_task(task)
        return {
            "success": True,
            "message": "Arrived at drop-off location.",
            "current_location": (current_lat, current_lng)
        }

    def initiate_wait_countdown(self, task_id: str) -> Dict[str, Any]:
        """Customer is unreachable by phone. Start 10-minute countdown."""
        task = self.repo.get_task_by_id(task_id)
        if not task:
            return {"success": False, "message": "Task not found"}
        
        task.start_10_min_countdown()
        self.repo.save_task(task)
        return {
            "success": True,
            "message": "Customer unreachable. 10-minute wait timer activated.",
            "wait_start": task.wait_start_time.isoformat()
        }

    def confirm_delivery_and_cod(self, task_id: str, amount_paid: float) -> Dict[str, Any]:
        """Customer receives order, pays cash (if COD) or signs confirmation."""
        task = self.repo.get_task_by_id(task_id)
        if not task:
            return {"success": False, "message": "Task not found"}
        
        order = self.repo.get_order_by_id(task.order_id)
        if not order:
            return {"success": False, "message": "Associated order not found"}

        # If order is COD, verify collected amount matches final amount
        if order.payment_method == "COD" and amount_paid < order.final_amount:
            return {
                "success": False,
                "message": f"COD amount insufficient! Expected {order.final_amount} VND, got {amount_paid} VND"
            }

        task.confirm_successful_delivery(amount_paid)
        self.repo.save_task(task)
        self.repo.update_order_status(task.order_id, "Delivered")
        
        # Credit delivery fee to shipper wallet (e.g. 20,000 VND earning)
        earnings = 20000.0
        self.repo.update_shipper_wallet(task.shipper_id, earnings)

        return {
            "success": True,
            "message": "Order successfully delivered! Wallet credited.",
            "order_status": "Delivered",
            "cod_collected": amount_paid,
            "shipper_credited": earnings
        }

    def record_delivery_failure(self, task_id: str, reason: str = "Customer unreachable after 10m") -> Dict[str, Any]:
        """Delivery aborted after 10-minute wait expires. Return to Hub."""
        task = self.repo.get_task_by_id(task_id)
        if not task:
            return {"success": False, "message": "Task not found"}

        task.mark_delivery_failed(reason)
        self.repo.save_task(task)
        self.repo.update_order_status(task.order_id, "Delivery_Failed", failure_reason=reason)

        return {
            "success": True,
            "message": "Delivery failed. Order marked as Delivery_Failed. Package must be returned to Hub.",
            "task_status": "Failed_Returned",
            "order_status": "Delivery_Failed",
            "reason": reason
        }
