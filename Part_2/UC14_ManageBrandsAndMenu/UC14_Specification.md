# Fully Developed Use Case Specification: UC14 - Manage brands and menu items
**Author:** Ngô Tấn Thành (MSSV: 524H0031)  
**Use Case ID:** UC14  
**Use Case Name:** Manage brands and menu items  

---

| Item | Content |
| :--- | :--- |
| **Use case name** | UC14: Manage brands and menu items |
| **Scenario / trigger** | Administrator needs to introduce a new virtual brand, create or update bilingual menu items, assign preparation stations, allocate operational hubs, or discontinue an item. |
| **Actors** | Administrator (primary actor). |
| **Related use cases** | • Preceding: UC13 (Manage hubs and kitchen capacity)<br>• Operational: UC9 (Manage menu item availability at a hub)<br>• Subsequent: UC2 (Browse hubs, brands and menus), UC3 (Place an order), UC7 (Confirm or reject an incoming order) |
| **Stakeholders and interests** | • **Administrator:** Demands centralized, accurate management of virtual brands, bilingual item details, pricing consistency, and hub allocations.<br>• **Virtual Brand Partners:** Expect accurate brand profiles, cuisine categorization, and correct menu listings across assigned hubs.<br>• **Kitchen Staff:** Require clear preparation station assignments (Wok, Fryer, Assembly, Beverage) so incoming order items go to the right kitchen station.<br>• **Customers (Local & Foreign):** Expect clear bilingual item names/descriptions, transparent prices, and accurate live menu availability. |
| **Pre-conditions** | 1. Administrator is authenticated with administrative privileges.<br>2. At least one active cloud kitchen hub and standard preparation stations exist in the system. |
| **Post-conditions** | 1. `Brand` and `MenuItem` records are created or updated in the system (a published `MenuItem` is in state `Active`; a retired `MenuItem` transitions to state `Discontinued`).<br>2. Each active `MenuItem` is linked to a valid preparation station and assigned operational hubs.<br>3. Updated brand and menu offerings are immediately available to customers and hub kitchens, and the administrative change is recorded. |

---

### Flow of Activities

| Step | Actor Action (Administrator) | Step | System Response (SaigonBite System) |
| :---: | :--- | :---: | :--- |
| **1** | Open brand and menu catalog. | **1.1** | Display virtual brands and hub assignments. |
| **2** | Select a virtual brand to configure (or create a new brand). | **2.1** | Display brand details, current menu items, and available preparation stations. |
| **3** | Enter brand details (name, cuisine type) and select assigned operational hubs. | **3.1** | Validate brand uniqueness and hub assignments, save brand details, and prompt for menu item updates. |
| **4** | Enter menu item details (item code, Vietnamese and English names, description, unit price, preparation station) or select an item to discontinue. | **4.1**<br><br>**4.2** | Validate item code uniqueness, positive unit price (> 0 VND), and station compatibility at assigned hubs.<br>Save the `MenuItem` (in state `Active` when published, or state `Discontinued` when retired), update hub menu offerings, and display confirmation summary. |

---

### Exception Conditions

- **3.1a Duplicate brand identifier:**
  1. System detects the brand name or code already exists and prompts the Administrator to correct the brand identifier.

- **3.1b Missing hub assignment:**
  1. System detects no operational cloud kitchen hub is assigned and prompts the Administrator to select at least one hub.

- **4.1a Duplicate item code:**
  1. System detects a menu item code collision and prompts the Administrator to enter a unique item code.

- **4.1b Invalid unit price (<= 0 VND):**
  1. System rejects a zero or negative price and prompts the Administrator to enter a positive unit price.

- **4.1c Incompatible preparation station:**
  1. System detects the chosen preparation station is unsupported at one or more assigned hubs and prompts the Administrator to adjust the station assignment.
