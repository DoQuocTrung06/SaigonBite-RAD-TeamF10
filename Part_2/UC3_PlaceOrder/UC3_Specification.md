# Fully Developed Use Case Specification: UC3 - Place an Order
**Author:** Ngô Tấn Thành (MSSV: 524H0031)  
**Use Case ID:** UC3  
**Use Case Name:** Place an order  

---

| Item | Content |
| :--- | :--- |
| **Use case name** | UC3: Place an order |
| **Scenario / trigger** | Customer completes multi-brand food selection from a cloud kitchen hub and initiates checkout. |
| **Actors** | Customer (primary actor), Payment Gateway (external payment authorization system). |
| **Related use cases** | • Preceding: UC2 (Browse hubs, brands and menus), UC14 (Manage brands and menu items)<br>• Supporting: UC15 (Manage vouchers)<br>• Subsequent: UC7 (Confirm or reject an incoming order), UC10 (Deliver an order) |
| **Stakeholders and interests** | • **Customer:** Desires a seamless multi-brand single-basket ordering experience, transparent distance-based delivery fees, valid voucher redemption, and accurate real-time order confirmation.<br>• **Virtual Restaurant Brands:** Desire accurate order assignment to specific preparation stations (Wok, Fryer, Assembly, Beverage) without item omissions.<br>• **SaigonBite Platform Operations:** Enforces single-hub constraints to avoid split shipments, ensures delivery quality within a 7.0 km radius, and balances kitchen workload through Quiet-Kitchen incentive discounts.<br>• **Shippers:** Expect orders routed strictly within reachable delivery zones with clear cash-on-delivery obligations. |
| **Pre-conditions** | 1. Customer is logged in and has selected menu items in the shopping basket.<br>2. Selected menu items are currently in state `Active` (available) at the chosen cloud kitchen hub.<br>3. Selected cloud kitchen hub is open and below its busy-capacity limit (active workload < 85%). |
| **Post-conditions** | 1. A new `Order` object is recorded in the system with initial state `Placed`.<br>2. Order line items and preparation station assignments are recorded and queued for hub kitchen confirmation.<br>3. Applicable discounts (at most one voucher discount and/or 10% Quiet-Kitchen discount) and the distance-based delivery fee are recorded on the order.<br>4. Payment status is recorded as `Paid` (online payment authorized) or `Unpaid` (Cash on Delivery in VND).<br>5. Customer receives an order confirmation receipt with order number, full price breakdown, and estimated arrival time (ETA). |

---

### Flow of Activities

| Step | Actor Action (Customer) | Step | System Response (SaigonBite System) |
| :---: | :--- | :---: | :--- |
| **1** | Customer reviews selected basket items and requests checkout. | **1.1** | System verifies that all basket items belong to the same cloud kitchen hub and displays the checkout summary. |
| **2** | Customer enters the delivery address. | **2.1** | System calculates the delivery distance from the hub, verifies distance <= 7.0 km, computes the delivery fee (15,000 VND for first 2 km + 5,000 VND per extra km), applies the 10% Quiet-Kitchen discount if hub workload < 40%, and displays the updated price summary. |
| **3** | Customer optionally enters a promotional voucher code. | **3.1** | If a voucher code is provided, System validates voucher eligibility and minimum spend, applies the discount, and displays the updated order total. |
| **4** | Customer selects a payment method (Cash on Delivery or Online Payment), provides payment details if paying online, and submits the order. | **4.1**<br><br>**4.2** | If Online Payment is selected, System requests payment authorization from the Payment Gateway and records payment as `Paid`; if Cash on Delivery is selected, System records payment as `Unpaid`.<br>System creates the `Order` in state `Placed`, queues preparation items for the hub kitchen, and returns the order confirmation receipt with order number and ETA. |

---

### Exception Conditions

- **1.1a Cross-hub basket conflict:**
  1. System detects basket items belonging to multiple physical cloud kitchen hubs.
  2. System informs the customer that a single order must come from one cloud kitchen hub and prompts the customer to adjust the basket.

- **2.1a Delivery distance exceeds 7.0 km:**
  1. System calculates route distance beyond the maximum 7.0 km delivery radius.
  2. System alerts the customer that the destination is outside the reachable service zone and prompts for an eligible delivery address.

- **3.1a Invalid or expired voucher:**
  1. System determines the voucher code is invalid, expired, or the order subtotal is below the minimum threshold.
  2. System notifies the customer and retains the pre-voucher total without blocking checkout.

- **4.1a Online payment authorization declined:**
  1. Payment Gateway declines the authorization request.
  2. System notifies the customer of the declined payment and offers to retry online payment or switch to Cash on Delivery (VND).
