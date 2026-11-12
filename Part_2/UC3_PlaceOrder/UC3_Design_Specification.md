# System Requirements Design Specification: UC3 - Place an Order
**Author:** Ngô Tấn Thành (MSSV: 524H0031)  
**Use Case ID:** UC3  
**Use Case Name:** Place an order  
**Methodology Reference:** Satzinger, Jackson & Burd, *Systems Analysis and Design in a Changing World*, 7th Edition (Chapters 4, 5, 12 & 13)

---

## 3.3.1 Design Classes in Detailed Design

Following the object-oriented multilayer design architecture (Satzinger, Jackson & Burd, 7e, Chapters 12 & 13, pp. 372–390, 408–425), problem domain classes from Section II (`Domain_Model_Class_Diagram`) are refined into software design classes:
- **Domain-Centric Attribute Naming & Types:** Attributes are private (`-`) using natural problem-domain nouns (`orderDateTime`, `dateRegistered`, `hubStatus`, `authorizationCode`, `itemNameVi`, `itemNameEn`), concise design types (`string`, `int`, `decimal`, `currency`, `date`, `boolean`), and `{key}` identifiers.
- **No Relational Foreign Keys or Redundant Reference Attributes:** Per Satzinger (7e, pp. 380–381, 421), foreign keys and object-reference attributes (such as `-myOrder: Order`) are omitted from attribute compartments and represented instead by **navigation visibility arrows (`-->`)**.
- **Pure 4-Layer Stereotypes:** Technical classes carry `«view»`, `«controller»`, or `«dataAccess»` stereotypes; problem domain classes omit `«entity»` stereotype clutter (Satzinger 7e, `Fig. 12-14`, `Fig. 12-24`, `Fig. 13-14`, `Fig. 13-24`).

### Layer 1: UI (View) Layer (`«view»`)

| Design Class | Stereotype | Attributes | Method Signatures (Public) |
| :--- | :--- | :--- | :--- |
| `CheckoutWindow` | `«view»` | *(None — UI controls)* | `+requestCheckout(basketItems): string`<br>`+enterDeliveryAddress(deliveryAddress): string`<br>`+applyVoucher(voucherCode): string`<br>`+authorizeOnlinePayment(paymentDetails): string`<br>`+submitOrder(paymentMethod): string`<br>`+displayOrderReceipt(orderId, receipt, eta): void` |

### Layer 2: Controller Layer (`«controller»`)

| Design Class | Stereotype | Attributes | Method Signatures (Public) |
| :--- | :--- | :--- | :--- |
| `OrderHandler` | `«controller»` | *(None — object references modeled via navigation visibility arrows)* | `+requestCheckout(basketItems): string`<br>`+enterDeliveryAddress(deliveryAddress): string`<br>`+applyVoucher(voucherCode): currency`<br>`+authorizeOnlinePayment(paymentDetails): string`<br>`+submitOrder(paymentMethod): Order` |

### Layer 3: Problem Domain Layer

| Design Class | Stereotype | Attributes (Private) | Method Signatures (Public) |
| :--- | :--- | :--- | :--- |
| `Customer` | *(Domain)* | `-customerId: string {key}`<br>`-fullName: string`<br>`-phoneNumber: string`<br>`-emailAddress: string`<br>`-dateRegistered: date` | *(Customer identity associated with `Order`)* |
| `Hub` | *(Domain)* | `-hubId: string {key}`<br>`-hubName: string`<br>`-address: string`<br>`-latitude: decimal`<br>`-longitude: decimal`<br>`-maxCapacityOrders: int`<br>`-hubStatus: string` | `+verifyHubCapacity(basketItems): boolean`<br>`+calculateDistance(deliveryAddress): decimal`<br>`+checkQuietKitchenDiscount(): boolean` |
| `Order` | *(Domain)* | `-orderId: string {key}`<br>`-orderDateTime: date`<br>`-orderStatus: string`<br>`-deliveryAddress: string`<br>`-distanceKm: decimal`<br>`-subtotal: currency`<br>`-deliveryFee: currency`<br>`-discountAmount: currency`<br>`-finalTotal: currency`<br>`-paymentMethod: string` | `+addOrderLine(item, qty, notes): OrderLine`<br>`+calculateSubtotal(): currency`<br>`+calculateDeliveryAndTotal(address, distanceKm, quietEligible): currency`<br>`+applyVoucherDiscount(voucherCode): currency`<br>`+authorizePayment(paymentDetails): string`<br>`+completeOrder(paymentMethod): string` |
| `OrderLine` | *(Domain)* | `-quantity: int`<br>`-itemPrice: currency`<br>`-lineTotal: currency`<br>`-specialNotes: string` | `+calculateLineTotal(item, qty): currency` |
| `MenuItem` | *(Domain)* | `-itemId: string {key}`<br>`-itemNameVi: string`<br>`-itemNameEn: string`<br>`-unitPrice: currency`<br>`-stationType: string`<br>`-status: string` | `+checkAvailability(): boolean` |
| `Voucher` | *(Domain)* | `-voucherCode: string {key}`<br>`-discountPercent: decimal`<br>`-maxDiscountAmount: currency`<br>`-minOrderAmount: currency`<br>`-startDate: date`<br>`-endDate: date`<br>`-usageQuota: int`<br>`-status: string` | `+calculateDiscount(voucherCode, subtotal): currency`<br>`+redeemVoucher(): void` |
| `Payment` | *(Domain)* | `-paymentId: string {key}`<br>`-paymentMethod: string`<br>`-paymentAmount: currency`<br>`-paymentStatus: string`<br>`-authorizationCode: string`<br>`-paymentDateTime: date` | `+authorizeOnlinePayment(paymentDetails, amount): string`<br>`+recordPayment(paymentMethod, amount): Payment` |
| `KitchenTicket` | *(Domain)* | `-ticketId: string {key}`<br>`-stationType: string`<br>`-status: string`<br>`-printedTime: date`<br>`-completedTime: date` | `+createStationTicket(stationType): KitchenTicket` |

### Layer 4: Data Access Layer (`«dataAccess»`)

| Design Class | Stereotype | Attributes | Method Signatures (Public) |
| :--- | :--- | :--- | :--- |
| `HubDA` | `«dataAccess»` | *(None)* | `+readHubForItems(basketItems): Hub` |
| `VoucherDA` | `«dataAccess»` | *(None)* | `+readVoucher(voucherCode): Voucher`<br>`+updateVoucher(voucher): boolean` |
| `PaymentDA` | `«dataAccess»` | *(None)* | `+createPayment(payment): boolean` |
| `OrderDA` | `«dataAccess»` | *(None)* | `+createOrder(order): string` |

---

## 3.3.2 Design Class Diagram (First-Cut DCD)

**Diagram File:** [UC3_FirstCut_DCD.png](file:///d:/project/pttkyc/SaigonBite-RAD-TeamF10/Part_2/UC3_PlaceOrder/UC3_FirstCut_DCD.png) (Source: [UC3_FirstCut_DCD.puml](file:///d:/project/pttkyc/SaigonBite-RAD-TeamF10/Part_2/UC3_PlaceOrder/UC3_FirstCut_DCD.puml))

Constructed strictly per Satzinger `Figure 12-14` (p. 382) and `Figure 13-14` (p. 413):
- **i. Domain design classes:** `Customer`, `Hub`, `Order`, `OrderLine`, `MenuItem`, `Voucher`, `Payment`, and `KitchenTicket` elaborated with private domain attributes, data types, `{key}` properties, and empty method compartments.
- **ii. Use case controller:** `«controller» OrderHandler` placed at the top of the navigation hierarchy with hierarchical visibility to the primary entry domain classes (`OrderHandler --> Customer`, `OrderHandler --> Hub`, `OrderHandler --> Order`).
- **iii. Navigation visibility:** Hierarchical low-coupling visibility arrows connecting primary classes to subordinate classes (`Customer --> Order`, `Hub --> Order`, `Order --> Voucher`, `Order --> Payment`, `Order --> KitchenTicket`, `Order --> OrderLine`, `OrderLine --> MenuItem`).

---

## 3.3.3 OOD with CRC Cards

Constructed per Satzinger `Figure 12-15` (p. 384) and `Figure 12-23` (p. 389): **Front** lists Class Name, Responsibilities (concise action phrases), and Collaborating Classes; **Back** lists Class Attributes.

### 1. `OrderHandler` (`«controller»`)

| Front — Responsibilities | Collaborating Classes |
| :--- | :--- |
| `requestCheckout()` — coordinate single-hub verification, line item creation, and subtotal calculation | `Hub`, `Order` |
| `enterDeliveryAddress()` — coordinate distance calculation, Quiet-Kitchen discount check, and order total calculation | `Hub`, `Order` |
| `applyVoucher()` — coordinate voucher discount calculation on order | `Order` |
| `authorizeOnlinePayment()` — coordinate online payment authorization | `Order` |
| `submitOrder()` — coordinate order completion, payment recording, ticket creation, and persistence | `Order` |

**Back — Attributes:** *(None — controller state held via navigation associations)*.

---

### 2. `CheckoutWindow` (`«view»`)

| Front — Responsibilities | Collaborating Classes |
| :--- | :--- |
| Capture customer checkout inputs (`requestCheckout()`, `enterDeliveryAddress()`, `applyVoucher()`, `authorizeOnlinePayment()`, `submitOrder()`) | `OrderHandler` |
| `displayOrderReceipt()` — render confirmation receipt (`orderId`, state `Placed`), fee summary, and ETA | `OrderHandler` |

**Back — Attributes:** *(None — UI controls)*.

---

### 3. `Order` *(Domain)*

| Front — Responsibilities | Collaborating Classes |
| :--- | :--- |
| `addOrderLine()` — instantiate `OrderLine` and verify item availability | `OrderLine` |
| `calculateSubtotal()` — sum line totals across basket items | `OrderLine` |
| `calculateDeliveryAndTotal()` — compute distance fee (`15,000 VND` first 2 km + `5,000 VND`/extra km) and 10% Quiet-Kitchen discount | `Hub` |
| `applyVoucherDiscount()` — validate voucher and apply discount to order total | `Voucher` |
| `authorizePayment()` — delegate online payment authorization | `Payment` |
| `completeOrder()` — transition state to `Placed`, record payment, redeem voucher, create station tickets, and persist order | `Payment`, `Voucher`, `KitchenTicket`, `OrderDA` |

**Back — Attributes:** `orderId {key}`, `orderDateTime`, `orderStatus`, `deliveryAddress`, `distanceKm`, `subtotal`, `deliveryFee`, `discountAmount`, `finalTotal`, `paymentMethod`.

---

### 4. `OrderLine` *(Domain)* & `MenuItem` *(Domain)*

| Class | Front — Responsibilities | Collaborating Classes | Back — Attributes |
| :--- | :--- | :--- | :--- |
| `OrderLine` | `calculateLineTotal()` — check item availability and compute `itemPrice * quantity` | `MenuItem` | `quantity`, `itemPrice`, `lineTotal`, `specialNotes` |
| `MenuItem` | `checkAvailability()` — verify item status is `Active` | *(None)* | `itemId {key}`, `itemNameVi`, `itemNameEn`, `unitPrice`, `stationType`, `status` |

---

### 5. `Hub` *(Domain)*

| Front — Responsibilities | Collaborating Classes |
| :--- | :--- |
| `verifyHubCapacity()` — read hub for basket items, verify single-hub rule and capacity < 85% | `HubDA` |
| `calculateDistance()` — calculate delivery distance and verify radius <= 7.0 km | *(None)* |
| `checkQuietKitchenDiscount()` — check whether current kitchen load < 40% | *(None)* |

**Back — Attributes:** `hubId {key}`, `hubName`, `address`, `latitude`, `longitude`, `maxCapacityOrders`, `hubStatus`.

---

### 6. `Voucher` *(Domain)*, `Payment` *(Domain)*, & `KitchenTicket` *(Domain)*

| Class | Front — Responsibilities | Collaborating Classes | Back — Attributes |
| :--- | :--- | :--- | :--- |
| `Voucher` | `calculateDiscount()` — read voucher by code, verify dates/quota/min order, compute discount<br>`redeemVoucher()` — decrement quota and persist update | `VoucherDA` | `voucherCode {key}`, `discountPercent`, `maxDiscountAmount`, `minOrderAmount`, `startDate`, `endDate`, `usageQuota`, `status` |
| `Payment` | `authorizeOnlinePayment()` — verify online payment authorization<br>`recordPayment()` — record `Paid` online transaction or `Unpaid` COD obligation and persist payment | `PaymentDA` | `paymentId {key}`, `paymentMethod`, `paymentAmount`, `paymentStatus`, `authorizationCode`, `paymentDateTime` |
| `KitchenTicket` | `createStationTicket()` — create station-routed preparation ticket (`Wok`, `Fryer`, `Assembly`, `Beverage`) | *(None)* | `ticketId {key}`, `stationType`, `status`, `printedTime`, `completedTime` |

---

### 7. Data Access Classes (`HubDA`, `VoucherDA`, `PaymentDA`, `OrderDA`) (`«dataAccess»`)

| Class | Front — Responsibilities | Collaborating Classes |
| :--- | :--- | :--- |
| `HubDA` | `readHubForItems()` — retrieve operational hub serving basket items | `Hub` |
| `VoucherDA` | `readVoucher()` — retrieve voucher by code<br>`updateVoucher()` — persist decremented voucher quota | `Voucher` |
| `PaymentDA` | `createPayment()` — persist payment record | `Payment` |
| `OrderDA` | `createOrder()` — persist finalized `Order`, `OrderLine` items, and `KitchenTicket` records | `Order`, `OrderLine`, `KitchenTicket` |

---

## 3.3.4 OOD with Sequence Diagram — Traceability from SSD

**Diagram File:** [UC3_Design_Sequence_Diagram.png](file:///d:/project/pttkyc/SaigonBite-RAD-TeamF10/Part_2/UC3_PlaceOrder/UC3_Design_Sequence_Diagram.png) (Source: [UC3_Design_Sequence_Diagram.puml](file:///d:/project/pttkyc/SaigonBite-RAD-TeamF10/Part_2/UC3_PlaceOrder/UC3_Design_Sequence_Diagram.puml))

Constructed per Satzinger `Figure 13-20` (p. 421) and `Figure 13-23` (p. 423) with View, Controller, Domain, and Data Access lifelines, UML activation bars, and inline message conditions (`*[for each item]`, `[voucher code provided]`, `[online payment selected]`):

| Section II SSD Input Message | Multilayer Sequence Realization (`View` -> `Controller` -> `Domain` -> `Data Access`) | Return Value to Actor |
| :--- | :--- | :--- |
| `requestCheckout(basketItems)` | `:CheckoutWindow` -> `:OrderHandler` -> `aH:Hub.verifyHubCapacity` (`:HubDA.readHubForItems`) -> `*[for each item] aO:Order.addOrderLine` -> `aOL:OrderLine.calculateLineTotal` (`aMI:MenuItem.checkAvailability`) -> `aO:Order.calculateSubtotal` | `checkout summary` |
| `enterDeliveryAddress(deliveryAddress)` | `:CheckoutWindow` -> `:OrderHandler` -> `aH:Hub.calculateDistance` -> `aH:Hub.checkQuietKitchenDiscount` -> `aO:Order.calculateDeliveryAndTotal` | `distance, delivery fee, price summary` |
| `applyVoucher(voucherCode)` | `:CheckoutWindow` -> `:OrderHandler` -> `aO:Order.applyVoucherDiscount` -> `aV:Voucher.calculateDiscount` (`:VoucherDA.readVoucher`) | `discount amount, updated total` |
| `authorizeOnlinePayment(paymentDetails)` | `:CheckoutWindow` -> `:OrderHandler` -> `aO:Order.authorizePayment` -> `aP:Payment.authorizeOnlinePayment` | `payment authorization` |
| `submitOrder(paymentMethod)` | `:CheckoutWindow` -> `:OrderHandler` -> `aO:Order.completeOrder` -> `aP:Payment.recordPayment` (`:PaymentDA.createPayment`) -> `[voucher applied] aV:Voucher.redeemVoucher` (`:VoucherDA.updateVoucher`) -> `aKT:KitchenTicket.createStationTicket` -> `:OrderDA.createOrder` -> `:CheckoutWindow.displayOrderReceipt` | `order number, state Placed, receipt, ETA` |

---

## 3.3.5 Final Design Class Diagram

**Diagram File:** [UC3_Final_DCD.png](file:///d:/project/pttkyc/SaigonBite-RAD-TeamF10/Part_2/UC3_PlaceOrder/UC3_Final_DCD.png) (Source: [UC3_Final_DCD.puml](file:///d:/project/pttkyc/SaigonBite-RAD-TeamF10/Part_2/UC3_PlaceOrder/UC3_Final_DCD.puml))

Constructed per Satzinger `Figure 12-24` (p. 389) and `Figure 13-24` (p. 425):
1. **Complete Method Signatures:** Every message in `UC3_Design_Sequence_Diagram` is added as a concise public method signature (`+methodName(param1, param2): returnType`) on its target class across `CheckoutWindow`, `OrderHandler`, `Hub`, `Order`, `OrderLine`, `MenuItem`, `Voucher`, `Payment`, `KitchenTicket`, `HubDA`, `VoucherDA`, `PaymentDA`, and `OrderDA`.
2. **Hierarchical Orthogonal Navigation Visibility:** Low-coupling unidirectional navigation arrows match the exact call hierarchy of the sequence diagram (`CheckoutWindow --> OrderHandler`, `OrderHandler --> Customer / Hub / Order`, `Hub --> HubDA`, `Order --> Voucher --> VoucherDA`, `Order --> Payment --> PaymentDA`, `Order --> KitchenTicket`, `Order --> OrderDA`, `Order --> OrderLine --> MenuItem`).
