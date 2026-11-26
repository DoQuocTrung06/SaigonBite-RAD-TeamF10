# SSD-to-UI MAPPING FOR UC7: CONFIRM OR REJECT AN INCOMING ORDER
**Author:** Đỗ Quốc Trung (`524H0132`)  
**Prototype File:** `Part_3/ui_prototype/UC7_KDS_Prototype.html`  
**Controller Reference:** `Part_3/src/csharp/Controllers/KitchenController.cs`

---

## Traceability Matrix: UC7 System Sequence Diagram (SSD) to KDSConsoleUI

| Step | SSD Message (Section 2.2.2) | Message Type | Mapped UI Component in `UC7_KDS_Prototype.html` | Mapped C# Controller / Domain Call |
| :---: | :--- | :---: | :--- | :--- |
| **1** | `displayIncomingOrders(hubId)` | System Return | Order cards grid (`#ordersGrid`) showing `ORD-001`, `ORD-002`, items, station routing, and live **120s SLA Timer** badge. | `OrderDAO.FindById(orderId)` |
| **2** | `checkHubWorkload(hubId)` | System Check | Top Hub Capacity Bar (`#hubBar`) showing `Active Capacity: X / 50 (%)` and `BUSY (>= 85% Throttled)` indicator. | `Hub.IsOverloaded()` (`>= 0.85`) |
| **3** | `confirmOrder(orderId, stationId)` | Actor Input | Single-tap **Confirm Order** button on the order card (satisfies NFR4 <= 2-tap KDS rule). | `KitchenController.ConfirmOrder(orderId, stationId, elapsedSeconds)` |
| **4** | `orderConfirmedAndTicketPrinted(orderId, ticketId)` | System Return | Status box updates to `Status: Confirmed | Address Locked: true | Ticket: KT_ORD-001` and appends entry to `#auditLog`. | `Order.UpdateStatus("Confirmed")` (`IsLocked = true`) & `KitchenTicketDAO.Save(ticket)` |
| **5** | `rejectOrder(orderId, reason)` | Actor Input | 2-tap workflow: Tap **Reject Order** button -> Select preset reason radio option in Modal (`#rejectModal`) -> Tap **Confirm Reject**. | `KitchenController.RejectOrder(orderId, reason)` |
| **6** | `orderCancelledAndRefundTriggered(orderId, reason)` | System Return | Status box updates to `Status: Cancelled | Rejection Reason: ... (Auto Refund Triggered)` and logs audit trail. | `Order.UpdateStatus("Cancelled", reason)` & `AuditLogDAO.RecordAuditEntry(...)` |
| **7** | `autoTimeoutOrder(orderId)` (120s elapsed) | Exception Event | Live countdown reaches `0s` -> card auto-transitions to `Cancelled` with timeout reason and audit log. | `elapsedSeconds > 120` branch in `KitchenController.ConfirmOrder(...)` |
