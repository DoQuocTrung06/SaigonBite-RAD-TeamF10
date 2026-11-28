# SSD-TO-UI TRACEABILITY SPECIFICATION (SECTION 4.3.3 UI DESIGN)
**Project:** SaigonBite Cloud-Kitchen Multi-Brand Food Delivery Hub (OFDH)  
**Team:** Team F10 (`524H0132`, `524H0031`, `524H0136`)  

---

## 1. UC3: Place an order — `CheckoutWindow` (Author: `524H0031` — Ngô Tấn Thành)
**Prototype File:** `Part_3/ui_prototype/UC3_CheckoutWindow_UI.html` (`UC3_CheckoutWindow_UI.png`)  
**View & Controller Classes:** `Part_3/src/Views/CheckoutWindow.cs` $\rightarrow$ `Part_3/src/Controllers/OrderHandler.cs`

| Step | SSD Message (Figure 2.4) | Direction | UI Component in `CheckoutWindow` | Mapped C# View & Controller Method | Business Rule Enforced on UI |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **1** | `requestCheckout(basketItems)` | Customer $\rightarrow$ System | **Multi-Brand Basket Table** & **Proceed to Checkout** trigger | `CheckoutWindow.requestCheckout(basketItems)` $\rightarrow$ `OrderHandler.requestCheckout(basketItems)` | Verifies single-hub rule (`1.1a`) and hub active load `< 85%` (`A-02`). |
| **1.1** | `checkout summary` | System $\rightarrow$ Customer | **Hub Status Header** (`Hub H01 — Load 30% < 85%`) & item line totals (`165,000 VND`) | `Order.addOrderLine(...)` & `Order.calculateSubtotal()` | Displays bilingual item names, preparation station tags, and initial subtotal. |
| **2** | `enterDeliveryAddress(deliveryAddress)` | Customer $\rightarrow$ System | **Delivery Address Input Box** (`45 Le Loi, District 1, HCMC`) | `CheckoutWindow.enterDeliveryAddress(address)` $\rightarrow$ `OrderHandler.enterDeliveryAddress(address)` | Calculates route distance from preparing hub (`3.2 km`) and checks `<= 7.0 km` (`2.1a`, `A-01`). |
| **2.1** | `distance, delivery fee, price summary` | System $\rightarrow$ Customer | **Price Breakdown Table** (`+25,000 VND` delivery fee; `-16,500 VND` Quiet-Kitchen 10% discount) | `Hub.calculateDistance(...)`, `Hub.checkQuietKitchenDiscount()` & `Order.calculateDeliveryAndTotal(...)` | Applies `15,000 VND` (first 2 km) + `5,000 VND/km` formula and automatic `10%` Quiet-Kitchen discount when hub load `< 40%` (`A-03`). |
| **3** | `applyVoucher(voucherCode)` (`opt`) | Customer $\rightarrow$ System | **Promo Voucher Input Field** (`SBWELCOME10`) & **Apply Voucher** button | `CheckoutWindow.applyVoucher(code)` $\rightarrow$ `OrderHandler.applyVoucher(code)` | Enforces at most 1 promotional voucher per order; retains pre-voucher total without blocking checkout if invalid (`3.1a`). |
| **3.1** | `discount amount, updated total` | System $\rightarrow$ Customer | **Voucher Discount Row** (`-16,500 VND`) & **Final Payable Total** (`157,000 VND`) | `Order.applyVoucherDiscount(code)` $\rightarrow$ `Voucher.calculateDiscount(code, subtotal)` | Displays updated total after combining Quiet-Kitchen and single voucher discounts. |
| **4** | `authorizeOnlinePayment(paymentDetails)` (`opt`) | Customer $\rightarrow$ System | **Payment Method Selector** (`Online Payment`) & **Authorize Online Card** button | `CheckoutWindow.authorizeOnlinePayment(details)` $\rightarrow$ `OrderHandler.authorizeOnlinePayment(details)` | Requests payment gateway authorization; offers retry or COD switch if declined (`4.1a`). |
| **4.1** | `payment authorization` | System $\rightarrow$ Customer | **Authorization Badge** (`AUTH-20261128-8841 — Paid`) | `Order.authorizePayment(details)` $\rightarrow$ `Payment.authorizeOnlinePayment(details, amount)` | Displays authorization code before order submission. |
| **5** | `submitOrder(paymentMethod)` | Customer $\rightarrow$ System | **Submit Order** primary action button | `CheckoutWindow.submitOrder(method)` $\rightarrow$ `OrderHandler.submitOrder(method)` | Creates `Order` in state `Placed`, records `Paid` or `Unpaid` (COD in VND, `A-04`), redeems voucher, and queues station tickets. |
| **5.1** | `order number, state Placed, receipt, ETA` | System $\rightarrow$ Customer | **Order Confirmation Receipt Panel** (`#ORD-001`, state `Placed`, tickets `KT-001..003`, `ETA: 25 mins`) | `CheckoutWindow.displayOrderReceipt(orderId, receipt, eta)` | Displays immutable receipt with station ticket breakdown and estimated arrival time. |

---

## 2. UC14: Manage brands and menu items — `BrandCatalogWindow` (Author: `524H0031` — Ngô Tấn Thành)
**Prototype File:** `Part_3/ui_prototype/UC14_BrandCatalogWindow_UI.html` (`UC14_BrandCatalogWindow_UI.png`)  
**View & Controller Classes:** `Part_3/src/Views/BrandCatalogWindow.cs` $\rightarrow$ `Part_3/src/Controllers/BrandCatalogHandler.cs`

| Step | SSD Message (Figure 2.7) | Direction | UI Component in `BrandCatalogWindow` | Mapped C# View & Controller Method | Business Rule Enforced on UI |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **1** | `openBrandCatalog()` | Administrator $\rightarrow$ System | **Virtual Brand Directory Table** & **Hub Assignment Columns** | `BrandCatalogWindow.openBrandCatalog()` $\rightarrow$ `BrandCatalogHandler.openBrandCatalog()` | Loads all virtual brands and active cloud kitchen hubs (`H01`, `H02`). |
| **1.1** | `brand list, hub assignments` | System $\rightarrow$ Administrator | **Brand Directory Rows** (`BR-01`, `BR-02`, `BR-03` with hub tags) | `Brand.getAllBrands()` & `Hub.getActiveHubs()` | Shows live brand statuses and assigned operational hubs. |
| **2** | `selectBrand(brandId)` | Administrator $\rightarrow$ System | **Selectable Brand Row** (`BR-01: Pho Saigon Heritage`) | `BrandCatalogWindow.selectBrand(brandId)` $\rightarrow$ `BrandCatalogHandler.selectBrand(brandId)` | Populates brand profile editor, bilingual menu items table, and supported kitchen stations. |
| **2.1** | `brand details, menu items, available stations` | System $\rightarrow$ Administrator | **Brand Profile Form** & **Live Bilingual Catalog Table** | `Brand.getBrandCatalog(brandId)` & `Hub.getAvailableStations(brandId)` | Displays bilingual VI/EN item names, prices, and available hub stations (`Wok, Fryer, Assembly, Beverage`). |
| **3** | `saveBrandDetails(brandName, cuisineType, assignedHubs)` | Administrator $\rightarrow$ System | **Brand Name / Cuisine Inputs**, **Hub Checkboxes**, & **Save Brand Details** button | `BrandCatalogWindow.saveBrandDetails(...)` $\rightarrow$ `BrandCatalogHandler.saveBrandDetails(...)` | Validates brand name uniqueness (`3.1a`) and requires at least one operational hub (`3.1b`). |
| **3.1** | `brand confirmation` | System $\rightarrow$ Administrator | **Brand Saved Status Banner** | `Brand.saveBrandProfile(...)` $\rightarrow$ `BrandDA.saveBrand(...)` | Confirms brand profile and hub assignments in `brands` and `brand_hubs`. |
| **4** | `saveMenuItem(itemCode, nameVi, nameEn, unitPrice, stationType)` | Administrator $\rightarrow$ System | **Bilingual Dish Form** (`PHO-01`, `Phở Bò Đặc Biệt`, `Special Wagyu Beef Pho`, `85,000 VND`, `Wok`) & **Publish Menu Item** button | `BrandCatalogWindow.saveMenuItem(...)` $\rightarrow$ `BrandCatalogHandler.saveMenuItem(...)` | Enforces unique item code (`4.1a`), positive price `> 0 VND` (`4.1b`), and station compatibility at assigned hubs (`4.1c`). |
| **4.1** | `updated menu catalog, state Active` | System $\rightarrow$ Administrator | **Catalog Row Badge** (`State: Active`) | `Hub.verifyStationSupport(...)` & `MenuItem.publishMenuItem(...)` | Persists dish in state `Active` (linked to `MenuItem` State Machine Figure 2.8). |
| **5** | `discontinueMenuItem(itemCode)` (`opt`) | Administrator $\rightarrow$ System | **Discontinue Selected Item** button on catalog row (`PHO-99`) | `BrandCatalogWindow.discontinueMenuItem(itemCode)` $\rightarrow$ `BrandCatalogHandler.discontinueMenuItem(itemCode)` | Retires menu item from customer ordering while preserving historical order records. |
| **5.1** | `confirmation, state Discontinued` | System $\rightarrow$ Administrator | **Catalog Row Badge** (`State: Discontinued`) | `Brand.discontinueBrandItem(itemCode)` $\rightarrow$ `MenuItem.discontinueItem(itemCode)` | Transitions dish state to `Discontinued` in `menu_items`. |

---

## 3. UC7: Confirm or reject an incoming order — `KDSConsoleUI` (Author: `524H0132` — Đỗ Quốc Trung)
**Prototype File:** `Part_3/ui_prototype/UC7_KDS_Prototype.html`  
**View & Controller Classes:** `Part_3/src/Views/KDSConsoleUI.cs` $\rightarrow$ `Part_3/src/Controllers/KitchenController.cs`

| Step | SSD Message (Section 2.2.2) | Direction | UI Component in `KDSConsoleUI` | Mapped C# Controller / Domain Call |
| :---: | :--- | :---: | :--- | :--- |
| **1** | `displayIncomingOrders(hubId)` | System $\rightarrow$ Kitchen Staff | Order cards grid (`#ordersGrid`) with station tags & live **120s SLA Timer** | `OrderDAO.FindById(orderId)` |
| **2** | `checkHubWorkload(hubId)` | System Check | Top Hub Capacity Bar (`#hubBar`) showing `Active Capacity (%)` & `85% Busy` badge | `Hub.IsOverloaded()` (`>= 0.85`) |
| **3** | `confirmOrder(orderId, stationId)` | Kitchen Staff $\rightarrow$ System | Single-tap **Confirm Order** button (48x48px touch target, `<= 2` taps per NFR4) | `KitchenController.ConfirmOrder(orderId, stationId, elapsedSeconds)` |
| **4** | `orderConfirmedAndTicketPrinted(...)` | System $\rightarrow$ Kitchen Staff | Status box updates to `Confirmed | Address Locked: true` & prints station ticket | `Order.UpdateStatus("Confirmed")` & `KitchenTicketDAO.Save(ticket)` |
| **5** | `rejectOrder(orderId, reason)` | Kitchen Staff $\rightarrow$ System | **Reject Order** button $\rightarrow$ Mandatory reason modal (`#rejectModal`) | `KitchenController.RejectOrder(orderId, reason)` |

---

## 4. UC10: Deliver an order — `ShipperMobileUI` (Author: `524H0136` — Nguyễn Quang Tựu)
**Prototype Image:** `Part_3/ui_prototype/UC10_Shipper_App_UI.png`  
**View & Controller Classes:** `Part_3/src/Views/ShipperMobileUI.cs` $\rightarrow$ `Part_3/src/Controllers/DeliveryController.cs`

| Step | SSD Message (Figure 2.10) | Direction | UI Component in `ShipperMobileUI` | Mapped C# Controller / Domain Call |
| :---: | :--- | :---: | :--- | :--- |
| **1** | `scanPackageQR(orderId, qrCode)` | Shipper $\rightarrow$ System | **SCR-01: Hub Package Pickup** QR Scanner viewfinder & Confirm button | `ShipperMobileUI.OnScanPickupQRClicked(...)` $\rightarrow$ `DeliveryController.ProcessPickupScan(...)` |
| **2** | `confirmDeliveryAndCOD(orderId, codAmount)` | Shipper $\rightarrow$ System | **SCR-04: COD Settlement** VND cash input box & **Confirm Delivery** button | `ShipperMobileUI.OnConfirmDeliveryClicked(...)` $\rightarrow$ `DeliveryController.RecordDeliverySuccess(...)` |
| **3** | `recordDeliveryFailure(orderId, reason)` | Shipper $\rightarrow$ System | **SCR-03: 10-Min Wait Timer** (`00:00` unlocked) **Report Failed Delivery** button | `ShipperMobileUI.OnReportFailureClicked(...)` $\rightarrow$ `DeliveryController.RecordDeliveryFailure(...)` |
