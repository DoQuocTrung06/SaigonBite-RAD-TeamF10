# HƯỚNG DẪN MÃ NGUỒN PHẦN MỀM (OOP SOURCE CODE) (PART 3)
**Thư mục lưu trữ:** `Part_3/src/`  
**Người phụ trách:** Cả 3 thành viên phụ trách các lớp nghiệp vụ tương ứng theo Final DCD Part 2.  

---

## 1. Yêu Cầu Cốt Lõi Của Giảng Viên (Mục 4.3.5 & Rubric Tiêu Chí 5)

> [!IMPORTANT]
> **Quy định Rubric chấm điểm Programming Model (6.0 điểm):**  
> Mã nguồn phải được tổ chức chuẩn theo **Kiến trúc 3 tầng (Three-Layer Architecture)** và **bắt buộc phải khớp 100% tên lớp, tên phương thức và thuộc tính đã thiết kế trong Final DCD (Mục 3.1 đến 3.6)** của Báo cáo Part 2!

- **Ngôn ngữ lập trình được hỗ trợ:** Theo gợi ý trong Template chính thức của Thầy (ví dụ: **C# (.NET)**, **Java**, hoặc **Python**). Nhóm có thể chọn **C#** (hoặc Java/Python) tùy theo thế mạnh của các thành viên, miễn là tuân thủ chặt chẽ nguyên lý hướng đối tượng (OOP) 3 tầng.

---

## 2. Bảng Danh Mục Tên Lớp Chuẩn Xác Khớp 100% Với Final DCD Part 2

| Use Case | Thành viên | View Layer («view») | Controller Layer («controller») | Domain Layer (Business Entities) | Data Access Layer («dataAccess») |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **UC15: Manage vouchers** | **Đỗ Quốc Trung** (`524H0132`) | `VoucherConsoleUI` | `VoucherController` | `Voucher` | `VoucherDAO`, `AuditLogDAO` |
| **UC7: Confirm/reject incoming order** | **Đỗ Quốc Trung** (`524H0132`) | `KDSConsoleUI` | `KitchenController` | `Order`, `KitchenTicket` | `OrderDAO`, `KitchenTicketDAO`, `AuditLogDAO` |
| **UC3: Place an order** | **Ngô Tấn Thành** (`524H0031`) | `CheckoutWindow` | `OrderHandler` | `Customer` (`LocalCustomer`, `ForeignTourist`), `Hub`, `Order`, `OrderLine`, `MenuItem`, `Voucher`, `Payment` | `OrderDA`, `HubDA`, `VoucherDA`, `MenuItemDA` |
| **UC14: Manage brands & menu** | **Ngô Tấn Thành** (`524H0031`) | `BrandCatalogWindow` | `BrandCatalogHandler` | `Brand`, `MenuItem`, `KitchenStation`, `Hub` | `BrandDA`, `MenuItemDA`, `HubDA` |
| **UC10: Deliver an order** | **Nguyễn Quang Tựu** (`524H0136`) | `ShipperMobileUI` | `DeliveryController` | `DeliveryTask`, `Order`, `Payment`, `Shipper` | `DeliveryTaskDAO`, `OrderDAO`, `AuditLogDAO` |
| **UC16: Produce management reports** | **Nguyễn Quang Tựu** (`524H0136`) | `ReportConsoleUI` | `ReportController` | `ManagementReport`, `Hub` | `ReportDAO`, `OrderDAO`, `AuditLogDAO` |

---

## 3. Cấu Trúc Thư Mục Mã Nguồn Đề Xuất (Theo C# / Java / Python)

### Cấu trúc dự án (Ví dụ cho C# .NET / Java / Python):
```text
Part_3/src/
├── Views/ (hoặc views/)
│   ├── KDSConsoleUI.*                  # Trung (UC7)
│   ├── VoucherConsoleUI.*              # Trung (UC15)
│   ├── CheckoutWindow.*                # Thành (UC3)
│   ├── BrandCatalogWindow.*            # Thành (UC14)
│   ├── ShipperMobileUI.*               # Tựu (UC10)
│   └── ReportConsoleUI.*               # Tựu (UC16)
├── Controllers/ (hoặc controllers/)
│   ├── KitchenController.*             # Trung (UC7)
│   ├── VoucherController.*             # Trung (UC15)
│   ├── OrderHandler.*                  # Thành (UC3)
│   ├── BrandCatalogHandler.*           # Thành (UC14)
│   ├── DeliveryController.*            # Tựu (UC10)
│   └── ReportController.*              # Tựu (UC16)
├── Domain/ (hoặc models/)
│   ├── Customer.* (LocalCustomer, ForeignTourist)
│   ├── Order.*
│   ├── OrderLine.*
│   ├── KitchenTicket.*
│   ├── MenuItem.*
│   ├── Brand.*
│   ├── Voucher.*
│   ├── DeliveryTask.*
│   ├── Shipper.*
│   ├── Hub.*
│   ├── KitchenStation.*
│   ├── Payment.*
│   └── ManagementReport.*
└── DataAccess/ (hoặc data_access/)
    ├── OrderDAO.* (hoặc OrderDA)
    ├── KitchenTicketDAO.*
    ├── VoucherDAO.* (hoặc VoucherDA)
    ├── BrandDA.*
    ├── MenuItemDA.*
    ├── DeliveryTaskDAO.*
    ├── ReportDAO.*
    └── AuditLogDAO.*
```

---

## 4. Quy Định Commit Trên GitHub (Checklist Mục 39)

- Barem yêu cầu **mỗi sinh viên phải có > 10 commits có ý nghĩa** trên GitHub.
- Khi commit mã nguồn các lớp, hãy đặt commit message rõ ràng kèm mã SV, ví dụ:
  - `feat(uc7): implement KitchenController and KDSConsoleUI with 120s timer (524H0132)`
  - `feat(uc3): implement OrderHandler and CheckoutWindow multi-brand pricing (524H0031)`
  - `feat(uc10): implement DeliveryController and ShipperMobileUI with COD flow (524H0136)`
