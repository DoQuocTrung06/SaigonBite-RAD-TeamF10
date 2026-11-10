# System Requirements Design Specification: UC14 - Manage Brands and Menu Items
**Author:** Ngô Tấn Thành (MSSV: 524H0031)  
**Use Case ID:** UC14  
**Use Case Name:** Manage brands and menu items  
**Methodology Reference:** Satzinger, Jackson & Burd, *Systems Analysis and Design in a Changing World*, 7th Edition (Chapters 4, 5, 12 & 13)

---

## 3.4.1 Design Classes in Detailed Design

Following the object-oriented multilayer design architecture (Satzinger, Jackson & Burd, 7e, Chapters 12 & 13, pp. 372–390, 408–425), problem domain classes from Section II (`Domain_Model_Class_Diagram`) are refined into software design classes:
- **Domain-Centric Attribute Naming & Types:** Attributes are private (`-`) using natural problem-domain nouns (`itemNameVi`, `itemNameEn`, `hubStatus`, `currentLoad`, `status`), concise design types (`string`, `int`, `currency`), and `{key}` identifiers.
- **No Relational Foreign Keys or Redundant Reference Attributes:** Per Satzinger (7e, pp. 380–381, 421), foreign keys and object-reference attributes (such as `-selectedBrand: Brand`) are omitted from attribute compartments and represented instead by **navigation visibility arrows (`-->`)**.
- **Pure 4-Layer Stereotypes:** Technical classes carry `«view»`, `«controller»`, or `«dataAccess»` stereotypes; problem domain classes omit `«entity»` stereotype clutter (Satzinger 7e, `Fig. 12-14`, `Fig. 12-24`, `Fig. 13-14`, `Fig. 13-24`).

### Layer 1: UI (View) Layer (`«view»`)

| Design Class | Stereotype | Attributes | Method Signatures (Public) |
| :--- | :--- | :--- | :--- |
| `BrandCatalogWindow` | `«view»` | *(None — UI controls)* | `+openBrandCatalog(): string`<br>`+selectBrand(brandId): string`<br>`+saveBrandDetails(brandName, cuisineType, assignedHubs): string`<br>`+saveMenuItem(itemCode, nameVi, nameEn, unitPrice, stationType): string`<br>`+discontinueMenuItem(itemCode): string` |

### Layer 2: Controller Layer (`«controller»`)

| Design Class | Stereotype | Attributes | Method Signatures (Public) |
| :--- | :--- | :--- | :--- |
| `BrandCatalogHandler` | `«controller»` | *(None — object references modeled via navigation visibility arrows)* | `+openBrandCatalog(): List`<br>`+selectBrand(brandId): Brand`<br>`+saveBrandDetails(brandName, cuisineType, assignedHubs): string`<br>`+saveMenuItem(itemCode, nameVi, nameEn, unitPrice, stationType): string`<br>`+discontinueMenuItem(itemCode): string` |

### Layer 3: Problem Domain Layer

| Design Class | Stereotype | Attributes (Private) | Method Signatures (Public) |
| :--- | :--- | :--- | :--- |
| `Brand` | *(Domain)* | `-brandId: string {key}`<br>`-brandName: string`<br>`-cuisineType: string`<br>`-status: string` | `+getAllBrands(): List`<br>`+getBrandCatalog(brandId): Brand`<br>`+saveBrandProfile(brandName, cuisineType, assignedHubs): string`<br>`+saveBrandMenuItem(itemCode, nameVi, nameEn, unitPrice, stationType): string`<br>`+discontinueBrandItem(itemCode): string` |
| `MenuItem` | *(Domain)* | `-itemId: string {key}`<br>`-itemNameVi: string`<br>`-itemNameEn: string`<br>`-description: string`<br>`-unitPrice: currency`<br>`-stationType: string`<br>`-status: string` | `+getBrandMenuItems(brandId): List`<br>`+publishMenuItem(itemCode, nameVi, nameEn, unitPrice, stationType): MenuItem`<br>`+discontinueItem(itemCode): boolean` |
| `Hub` | *(Domain)* | `-hubId: string {key}`<br>`-hubName: string`<br>`-address: string`<br>`-maxCapacityOrders: int`<br>`-hubStatus: string` | `+getActiveHubs(): List`<br>`+getAvailableStations(brandId): List`<br>`+verifyStationSupport(stationType): boolean` |
| `KitchenStation` | *(Domain)* | `-stationId: string {key}`<br>`-stationName: string`<br>`-stationType: string`<br>`-currentLoad: int`<br>`-capacityLimit: int` | `+checkStationType(stationType): boolean` |

### Layer 4: Data Access Layer (`«dataAccess»`)

| Design Class | Stereotype | Attributes | Method Signatures (Public) |
| :--- | :--- | :--- | :--- |
| `BrandDA` | `«dataAccess»` | *(None)* | `+readAllBrands(): List`<br>`+readBrand(brandId): Brand`<br>`+saveBrand(brand, assignedHubs): string` |
| `HubDA` | `«dataAccess»` | *(None)* | `+readActiveHubs(): List`<br>`+readHubsByBrand(brandId): List` |
| `MenuItemDA` | `«dataAccess»` | *(None)* | `+readMenuItemsByBrand(brandId): List`<br>`+saveMenuItem(brandId, item): boolean`<br>`+updateMenuItemStatus(itemCode, status): boolean` |

---

## 3.4.2 Design Class Diagram (First-Cut DCD)

**Diagram File:** [UC14_FirstCut_DCD.png](file:///d:/project/pttkyc/SaigonBite-RAD-TeamF10/Part_2/UC14_ManageBrandsAndMenu/UC14_FirstCut_DCD.png) (Source: [UC14_FirstCut_DCD.puml](file:///d:/project/pttkyc/SaigonBite-RAD-TeamF10/Part_2/UC14_ManageBrandsAndMenu/UC14_FirstCut_DCD.puml))

Constructed strictly per Satzinger `Figure 12-14` (p. 382) and `Figure 13-14` (p. 413):
- **i. Domain design classes:** `Brand`, `MenuItem`, `Hub`, and `KitchenStation` elaborated with private domain attributes, data types, `{key}` properties, and empty method compartments.
- **ii. Use case controller:** `«controller» BrandCatalogHandler` placed at the top of the navigation hierarchy with direct visibility to the primary entry domain classes (`BrandCatalogHandler --> Brand`, `BrandCatalogHandler --> Hub`).
- **iii. Navigation visibility:** Hierarchical low-coupling visibility arrows connecting `Brand --> Hub`, `Brand --> MenuItem`, and `Hub --> KitchenStation`.

---

## 3.4.3 OOD with CRC Cards

Constructed per Satzinger `Figure 12-15` (p. 384) and `Figure 12-23` (p. 389): **Front** lists Class Name, Responsibilities (concise action phrases), and Collaborating Classes; **Back** lists Class Attributes.

### 1. `BrandCatalogHandler` (`«controller»`)

| Front — Responsibilities | Collaborating Classes |
| :--- | :--- |
| `openBrandCatalog()` — retrieve virtual brands and active operational hubs | `Brand`, `Hub` |
| `selectBrand()` — load selected brand catalog, bilingual menu items, and available stations | `Brand`, `Hub` |
| `saveBrandDetails()` — coordinate brand profile validation and persistence | `Brand` |
| `saveMenuItem()` — verify hub station compatibility and delegate item publication to brand | `Hub`, `Brand` |
| `discontinueMenuItem()` — coordinate menu item discontinuation | `Brand` |

**Back — Attributes:** *(None — controller state held via navigation associations)*.

---

### 2. `BrandCatalogWindow` (`«view»`)

| Front — Responsibilities | Collaborating Classes |
| :--- | :--- |
| Capture Administrator catalog events (`openBrandCatalog()`, `selectBrand()`, `saveBrandDetails()`, `saveMenuItem()`, `discontinueMenuItem()`) | `BrandCatalogHandler` |
| Render brand list, bilingual menu catalog, station options, validation error alerts, and state confirmations (`Active`, `Discontinued`) | `BrandCatalogHandler` |

**Back — Attributes:** *(None — UI controls)*.

---

### 3. `Brand` *(Domain)*

| Front — Responsibilities | Collaborating Classes |
| :--- | :--- |
| `getAllBrands()` — retrieve directory of virtual brands | `BrandDA` |
| `getBrandCatalog()` — load brand profile and associated bilingual menu items | `BrandDA`, `MenuItem` |
| `saveBrandProfile()` — validate brand details and non-empty hub assignment, and persist brand | `BrandDA`, `Hub` |
| `saveBrandMenuItem()` — delegate item publication and link item to brand | `MenuItem` |
| `discontinueBrandItem()` — delegate menu item discontinuation | `MenuItem` |

**Back — Attributes:** `brandId {key}`, `brandName`, `cuisineType`, `status`.

---

### 4. `MenuItem` *(Domain)*

| Front — Responsibilities | Collaborating Classes |
| :--- | :--- |
| `getBrandMenuItems()` — load all menu items belonging to a brand | `MenuItemDA` |
| `publishMenuItem()` — verify unique item code, bilingual names, and positive price (> 0 VND), set `status = Active`, and persist item | `MenuItemDA` |
| `discontinueItem()` — set `status = Discontinued` and persist status change | `MenuItemDA` |

**Back — Attributes:** `itemId {key}`, `itemNameVi`, `itemNameEn`, `description`, `unitPrice`, `stationType`, `status`.

---

### 5. `Hub` *(Domain)* & `KitchenStation` *(Domain)*

| Class | Front — Responsibilities | Collaborating Classes | Back — Attributes |
| :--- | :--- | :--- | :--- |
| `Hub` | `getActiveHubs()` — retrieve operational hubs<br>`getAvailableStations()` — load hubs assigned to brand and list supported stations<br>`verifyStationSupport()` — verify whether assigned hub supports target station type | `HubDA`, `KitchenStation` | `hubId {key}`, `hubName`, `address`, `maxCapacityOrders`, `hubStatus` |
| `KitchenStation` | `checkStationType()` — check whether station matches requested category (`Wok`, `Fryer`, `Assembly`, `Beverage`) | *(None)* | `stationId {key}`, `stationName`, `stationType`, `currentLoad`, `capacityLimit` |

---

### 6. Data Access Classes (`BrandDA`, `HubDA`, `MenuItemDA`) (`«dataAccess»`)

| Class | Front — Responsibilities | Collaborating Classes |
| :--- | :--- | :--- |
| `BrandDA` | `readAllBrands()`, `readBrand()`, `saveBrand()` — read and persist virtual brand records and hub assignments | `Brand` |
| `HubDA` | `readActiveHubs()`, `readHubsByBrand()` — read active operational hubs and brand-hub assignments | `Hub` |
| `MenuItemDA` | `readMenuItemsByBrand()`, `saveMenuItem()`, `updateMenuItemStatus()` — read and persist bilingual menu item records | `MenuItem` |

---

## 3.4.4 OOD with Sequence Diagram — Traceability from SSD

**Diagram File:** [UC14_Design_Sequence_Diagram.png](file:///d:/project/pttkyc/SaigonBite-RAD-TeamF10/Part_2/UC14_ManageBrandsAndMenu/UC14_Design_Sequence_Diagram.png) (Source: [UC14_Design_Sequence_Diagram.puml](file:///d:/project/pttkyc/SaigonBite-RAD-TeamF10/Part_2/UC14_ManageBrandsAndMenu/UC14_Design_Sequence_Diagram.puml))

Constructed per Satzinger `Figure 13-20` (p. 421) and `Figure 13-23` (p. 423) with View, Controller, Domain, and Data Access lifelines, UML activation bars, and inline message conditions (`[valid brand details]`, `[valid item details]`, `[discontinue item]`):

| Section II SSD Input Message | Multilayer Sequence Realization (`View` -> `Controller` -> `Domain` -> `Data Access`) | Return Value to Actor |
| :--- | :--- | :--- |
| `openBrandCatalog()` | `:BrandCatalogWindow` -> `:BrandCatalogHandler` -> `aB:Brand.getAllBrands` (`:BrandDA.readAllBrands`) & `aH:Hub.getActiveHubs` (`:HubDA.readActiveHubs`) | `brand list, hub assignments` |
| `selectBrand(brandId)` | `:BrandCatalogWindow` -> `:BrandCatalogHandler` -> `aB:Brand.getBrandCatalog` (`:BrandDA.readBrand`, `aMI:MenuItem.getBrandMenuItems` -> `:MenuItemDA.readMenuItemsByBrand`) -> `aH:Hub.getAvailableStations` (`:HubDA.readHubsByBrand`) | `brand details, menu items, available stations` |
| `saveBrandDetails(brandName, cuisineType, assignedHubs)` | `:BrandCatalogWindow` -> `:BrandCatalogHandler` -> `aB:Brand.saveBrandProfile` -> `[valid brand details] :BrandDA.saveBrand` | `brand confirmation` |
| `saveMenuItem(itemCode, nameVi, nameEn, unitPrice, stationType)` | `:BrandCatalogWindow` -> `:BrandCatalogHandler` -> `aH:Hub.verifyStationSupport` (`aKS:KitchenStation.checkStationType`) -> `aB:Brand.saveBrandMenuItem` -> `aMI:MenuItem.publishMenuItem` (`[valid item details] :MenuItemDA.saveMenuItem`) | `updated menu catalog, state Active` |
| `discontinueMenuItem(itemCode)` | `:BrandCatalogWindow` -> `:BrandCatalogHandler` -> `aB:Brand.discontinueBrandItem` -> `aMI:MenuItem.discontinueItem` -> `:MenuItemDA.updateMenuItemStatus` | `confirmation, state Discontinued` |

---

## 3.4.5 Final Design Class Diagram

**Diagram File:** [UC14_Final_DCD.png](file:///d:/project/pttkyc/SaigonBite-RAD-TeamF10/Part_2/UC14_ManageBrandsAndMenu/UC14_Final_DCD.png) (Source: [UC14_Final_DCD.puml](file:///d:/project/pttkyc/SaigonBite-RAD-TeamF10/Part_2/UC14_ManageBrandsAndMenu/UC14_Final_DCD.puml))

Constructed per Satzinger `Figure 12-24` (p. 389) and `Figure 13-24` (p. 425):
1. **Complete Method Signatures:** Every message in `UC14_Design_Sequence_Diagram` is added as a concise public method signature (`+methodName(param1, param2): returnType`) on its target class across `BrandCatalogWindow`, `BrandCatalogHandler`, `Brand`, `MenuItem`, `Hub`, `KitchenStation`, `BrandDA`, `HubDA`, and `MenuItemDA`.
2. **Hierarchical Orthogonal Navigation Visibility:** Low-coupling unidirectional navigation arrows match the exact call hierarchy of the sequence diagram (`BrandCatalogWindow --> BrandCatalogHandler`, `BrandCatalogHandler --> Brand / Hub`, `Brand --> BrandDA`, `Brand --> Hub --> HubDA`, `Brand --> MenuItem --> MenuItemDA`, `Hub --> KitchenStation`).
