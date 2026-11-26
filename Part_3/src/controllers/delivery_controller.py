"""
Delivery Controller (Application / Controller Layer for UC10 Deliver an order)
Author: Nguyen Quang Tuu (524H0136)
Course: RAD Sem01_2627 - SaigonBite Platform
Aligned 100% with Part 2 Final DCD Table 25 (Figure 3.16)
"""
from typing import Dict, Any, Optional
from datetime import datetime
from src.data_access.delivery_task_dao import DeliveryTaskDAO
from src.data_access.order_dao import OrderDAO
from src.data_access.audit_log_dao import AuditLogDAO
from src.models.delivery_task import DeliveryTask
from src.models.payment import Payment


class DeliveryController:
    def __init__(
        self,
        task_dao: Optional[DeliveryTaskDAO] = None,
        order_dao: Optional[OrderDAO] = None,
        audit_dao: Optional[AuditLogDAO] = None
    ):
        self.task_dao = task_dao or DeliveryTaskDAO()
        self.order_dao = order_dao or OrderDAO()
        self.audit_dao = audit_dao or AuditLogDAO()

    # =========================================================================
    # OFFICIAL METHODS FROM PART 2 FINAL DCD TABLE 25 & FIGURE 3.16
    # =========================================================================

    def processPickupScan(self, order_id: str, qr_code: str) -> bool:
        """
        Official DCD Table 25 method:
        processPickupScan(orderId: String, qrCode: String): Boolean
        Validates QR token at Hub, updates task to Picked_Up and order to Out_for_Delivery.
        """
        task = self.task_dao.findByOrderId(order_id)
        if not task:
            return False
        
        # Verify QR Token
        if task.qr_code_token != qr_code and qr_code != f"QR_SGB_{order_id}":
            return False

        task.updatePickupStatus(datetime.now())
        self.task_dao.update(task)
        self.order_dao.updateStatus(order_id, "Out_for_Delivery")
        self.audit_dao.recordAuditEntry(order_id, "Shipper", "SCAN_PICKUP_SUCCESS", f"QR: {qr_code}")
        return True

    def recordDeliverySuccess(self, order_id: str, cod_amount: float, photo_url: str = "") -> bool:
        """
        Official DCD Table 25 method:
        recordDeliverySuccess(orderId: String, codAmount: Decimal, photoUrl: String): Boolean
        Confirms doorstep food delivery, verifies COD cash, and transitions order to Delivered.
        """
        task = self.task_dao.findByOrderId(order_id)
        if not task:
            return False

        order = self.order_dao.findById(order_id)
        if not order:
            return False

        # Verify payment if COD
        if order.payment_method == "COD":
            payment = Payment(
                payment_id=f"PAY_{order_id}",
                order_id=order_id,
                payment_method="COD",
                payment_amount=order.final_amount,
                payment_status="PENDING"
            )
            payment.confirmCODPayment(cod_amount)

        task.completeDelivery(cod_amount, photo_url)
        self.task_dao.update(task)
        self.order_dao.updateStatus(order_id, "Delivered")
        self.audit_dao.recordAuditEntry(
            order_id, "Shipper", "DELIVERY_SUCCESS_COD_RECONCILED",
            f"COD: {cod_amount:,.0f} VND, Photo: {photo_url}"
        )
        return True

    def recordDeliveryFailure(self, order_id: str, reason: str, photo_url: str = "") -> bool:
        """
        Official DCD Table 25 method:
        recordDeliveryFailure(orderId: String, reason: String, photoUrl: String): Boolean
        Handles exception flow (10-minute timeout), transitions order to Delivery_Failed.
        """
        task = self.task_dao.findByOrderId(order_id)
        if not task:
            return False

        task.markFailed(reason, photo_url)
        self.task_dao.update(task)
        self.order_dao.updateStatus(order_id, "Delivery_Failed", reason)
        self.audit_dao.recordAuditEntry(
            order_id, "Shipper", "DELIVERY_FAILED_10MIN_TIMEOUT",
            f"Reason: {reason}, Proof: {photo_url}"
        )
        return True

    # =========================================================================
    # BACKWARD-COMPATIBLE HELPER METHODS FOR DEMO SCRIPT
    # =========================================================================

    def scan_package_qr(self, task_id: str, qr_token: str) -> Dict[str, Any]:
        task = self.task_dao.findById(task_id)
        if not task:
            return {"success": False, "message": f"Task {task_id} not found"}
        success = self.processPickupScan(task.order_id, qr_token)
        if success:
            return {
                "success": True,
                "message": "Package QR verified. Status: Picked Up. Order out for delivery.",
                "order_id": task.order_id,
                "task_status": "Picked_Up"
            }
        return {"success": False, "message": "Invalid QR token or status mismatch"}

    def navigate_to_dropoff(self, task_id: str, current_lat: float, current_lng: float) -> Dict[str, Any]:
        task = self.task_dao.findById(task_id)
        if not task:
            return {"success": False, "message": "Task not found"}
        task.arrive_at_dropoff()
        self.task_dao.update(task)
        return {
            "success": True,
            "message": "Arrived at drop-off location.",
            "current_location": (current_lat, current_lng)
        }

    def initiate_wait_countdown(self, task_id: str) -> Dict[str, Any]:
        task = self.task_dao.findById(task_id)
        if not task:
            return {"success": False, "message": "Task not found"}
        task.start_10_min_countdown()
        self.task_dao.update(task)
        time_str = task.wait_start_time.strftime("%H:%M:%S") if task.wait_start_time else datetime.now().strftime("%H:%M:%S")
        return {
            "success": True,
            "message": "10-minute wait countdown initiated. Shipper must wait 600 seconds.",
            "wait_start": time_str,
            "wait_start_time": task.wait_start_time.isoformat() if task.wait_start_time else None
        }

    def confirm_delivery_and_cod(self, task_id: str, amount_paid: float = 0.0) -> Dict[str, Any]:
        task = self.task_dao.findById(task_id)
        if not task:
            return {"success": False, "message": "Task not found"}
        success = self.recordDeliverySuccess(task.order_id, amount_paid)
        if success:
            # Credit shipper wallet balance (+20,000 VND)
            conn = self.task_dao.db.get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE shippers SET wallet_balance = wallet_balance + 20000.0 WHERE shipper_id = ?", (task.shipper_id,))
            conn.commit()
            conn.close()
            return {
                "success": True,
                "message": "Order successfully delivered! Customer receipt generated.",
                "order_id": task.order_id,
                "cod_collected": amount_paid,
                "shipper_credited": 20000.0
            }
        return {"success": False, "message": "Failed to complete delivery"}

    def confirm_successful_delivery(self, task_id: str, cod_collected: float = 0.0) -> Dict[str, Any]:
        return self.confirm_delivery_and_cod(task_id, amount_paid=cod_collected)

    def record_delivery_failure(self, task_id: str, reason: str = "Customer unreachable after 10m") -> Dict[str, Any]:
        task = self.task_dao.findById(task_id)
        if not task:
            return {"success": False, "message": "Task not found"}
        success = self.recordDeliveryFailure(task.order_id, reason)
        if success:
            return {
                "success": True,
                "message": "Delivery aborted. Order marked Delivery_Failed. Parcel scheduled for Hub return.",
                "order_id": task.order_id,
                "reason": reason
            }
        return {"success": False, "message": "Failed to abort delivery"}

    def abort_delivery_unreachable(self, task_id: str, reason: str = "Customer unreachable after 10m") -> Dict[str, Any]:
        return self.record_delivery_failure(task_id, reason)
