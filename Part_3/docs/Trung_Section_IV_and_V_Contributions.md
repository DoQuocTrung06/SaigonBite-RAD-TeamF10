# NỘI DUNG ĐÓNG GÓP MỤC IV & MỤC V BÁO CÁO BRS/SRS (PART 3)
**Tác giả:** Đỗ Quốc Trung (MSSV: `524H0132`) — Project Manager & Architect  
**Đơn vị:** Team F10 — Đồ án Phân tích và Thiết kế Yêu cầu (RAD Sem01_2627)  
**Tài liệu:** Đóng góp trực tiếp cho Báo cáo chính `TeamF10_BRS_SRS_for_SaigonBite.docx`

---

## 4.3.1 Map Persistent Objects to the Tables in a Database

Theo mô hình Miền (Domain Model Class Diagram – Mục 2.1.7) và Ma trận CRUD (Mục 2.3), toàn bộ các thực thể bền vững (Persistent Classes) được ánh xạ sang lược đồ cơ sở dữ liệu quan hệ `saigonbite_db` trong `Part_3/database/schema.sql` theo 4 quy tắc chuẩn hóa:

1. **Ánh xạ Kế thừa (Generalization Mapping — Feedback Log A-04):** Lớp cha `Customer` được ánh xạ theo mô hình **Table-per-Subtype** thành bảng chính `customers` (`customer_id`, `full_name`, `customer_type`) và hai bảng con `local_customers` (`phone_number`) cùng `foreign_tourists` (`passport_number`, `email_address`, `preferred_language`), liên kết 1-1 qua `FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE`.
2. **Ánh xạ Hợp thành (Whole-Part Composition):** Quan hệ Whole-Part giữa `Hub` và `KitchenStation`, giữa `Brand` và `MenuItem`, và giữa `Order` và `KitchenTicket` sử dụng khóa ngoại kèm `ON DELETE CASCADE` để đảm bảo vòng đời phụ thuộc chặt chẽ.
3. **Ánh xạ Lớp kết hợp (Association Class Mapping):** Lớp `OrderLine` phân rã quan hệ nhiều-nhiều giữa `Order` và `MenuItem` thành bảng `order_lines` với `quantity > 0`, `unit_price > 0` và `subtotal`.
4. **Ràng buộc nghiệp vụ (Business CHECK Constraints) & Xóa mềm:** Bảng `orders` khóa bán kính phục vụ `CHECK (distance_km > 0 AND distance_km <= 7.0)`; bảng `vouchers` dùng cột `status = 'Archived'` thay cho `DELETE` cứng nhằm bảo toàn khóa ngoại và nhật ký kiểm toán `audit_logs`.

| Lớp Domain (Part 2) | Bảng CSDL (`schema.sql`) | Khóa chính (PK) | Khóa ngoại (FK) & Ràng buộc chính |
| :--- | :--- | :--- | :--- |
| `Hub` | `hubs` | `hub_id` | `max_capacity_orders`, `is_busy` (cờ quá tải $\ge$ 85%) |
| `KitchenStation` | `kitchen_stations` | `station_id` | FK `hub_id` $\rightarrow$ `hubs` (`ON DELETE CASCADE`) |
| `Brand` | `brands` | `brand_id` | `status` (`ACTIVE` / `INACTIVE`) |
| `MenuItem` | `menu_items` | `item_id` | FK `brand_id` $\rightarrow$ `brands`, `CHECK (unit_price > 0)` |
| `Customer` | `customers` | `customer_id` | `CHECK (customer_type IN ('Local', 'Foreign'))` |
| `LocalCustomer` | `local_customers` | `customer_id` | FK `customer_id` $\rightarrow$ `customers`, `phone_number UNIQUE` |
| `ForeignTourist` | `foreign_tourists` | `customer_id` | FK `customer_id` $\rightarrow$ `customers`, `passport_number UNIQUE` |
| `Voucher` | `vouchers` | `voucher_code` | `CHECK (discount_percent >= 0 AND discount_percent <= 100)` |
| `Order` | `orders` | `order_id` | FK `customer_id`, `hub_id`, `voucher_code`; `CHECK (distance_km <= 7.0)` |
| `OrderLine` | `order_lines` | `order_line_id` | FK `order_id`, `item_id`; `CHECK (quantity > 0)` |
| `KitchenTicket` | `kitchen_tickets` | `ticket_id` | FK `order_id`, `station_id` |
| `AuditLog` | `audit_logs` | `log_id` | `AUTO_INCREMENT`, lưu dấu vết bất biến theo NFR5 (< 1s) |

---

## 4.3.2 Modifying Sequence Diagrams (Bổ sung tầng Data Access cho UC15 & UC7)

Hai sơ đồ tuần tự thiết kế của **UC15 (Manage vouchers)** và **UC7 (Confirm or reject an incoming order)** được cập nhật tầng Data Access và Database tương tác trực tiếp (`Figure_4_3_2_UC15_Modified_Sequence_Diagram.puml` và `Figure_4_3_2_UC7_Modified_Sequence_Diagram.puml`):

- **UC15 (`VoucherController`):** Tương tác tuần tự qua `VoucherDAO.FindByCode()` (`SELECT` kiểm tra trùng mã) $\rightarrow$ `Voucher.Validate()` $\rightarrow$ `VoucherDAO.Save()` (`INSERT INTO vouchers`) và `AuditLogDAO.RecordAuditEntry()` (`INSERT INTO audit_logs`). Chức năng lưu trữ mềm gọi `Voucher.Archive()` cập nhật `status = 'Archived'`.
- **UC7 (`KitchenController`):** Khi bếp trưởng bấm `ConfirmOrder()` trong giới hạn SLA 120 giây, `KitchenController` đọc `OrderDAO.FindById()` và `HubDAO.FindById()`, kiểm tra ngưỡng quá tải `Hub.IsOverloaded()` ($\ge$ 85%), cập nhật `OrderDAO.UpdateStatus(orderId, "Confirmed")` (tự động bật `IsLocked = true`), lưu `KitchenTicketDAO.Save()` xuống bảng `kitchen_tickets`, và ghi nhật ký `AuditLogDAO`. Nhánh từ chối `RejectOrder()` hoặc quá hạn 120s chuyển đơn sang `Cancelled` và ghi log kích hoạt hoàn tiền tự động.

---

## 4.3.4 SQL Code

Toàn bộ mã nguồn SQL được lưu tại thư mục `Part_3/database/` với đầy đủ 3 phần theo yêu cầu:
1. **i. Create database (`Part_3/database/schema.sql`):** Lệnh `CREATE DATABASE IF NOT EXISTS saigonbite_db; USE saigonbite_db;`.
2. **ii. Create tables (`Part_3/database/schema.sql`):** Tạo 14 bảng quan hệ kèm đầy đủ `PRIMARY KEY`, `FOREIGN KEY`, và `CHECK` constraints khớp với Mục 4.3.1.
3. **iii. Sample data (`Part_3/database/seed.sql`):** Nạp dữ liệu mẫu cho 2 Hubs (`H01` tải 40% bình thường, `H02` cờ `is_busy = TRUE`), 3 trạm bếp, 2 thương hiệu, 3 món ăn song ngữ, khách hàng `LocalCustomer` & `ForeignTourist`, voucher (`SBWELCOME10`, `QUIET10`), và các đơn hàng `ORD-001`, `ORD-002` ở trạng thái `Pending_Kitchen`.

---

## 5.1 Test Plan and Test Cases (Bảng Kiểm thử UC15 & UC7)

*(Chi tiết bảng 8 cột được lưu tại `Part_3/tests/Test_Cases_UC15_UC7.md` và chạy kiểm chứng trực tiếp qua `Program.cs`)*

- `TC_UC15_01`: Tạo mới voucher `QUIET10` hợp lệ, xác minh lưu trạng thái `Active` và ghi `AuditLog` $\rightarrow$ **PASS**
- `TC_UC7_01`: Bếp xác nhận `ORD-001` trong 45s ($\le$ 120s) $\rightarrow$ `Confirmed`, khóa cứng đơn `IsLocked = True`, sinh phiếu `KT_ORD-001` $\rightarrow$ **PASS**
- `TC_UC7_02`: Bếp từ chối `ORD-002` kèm lý do `Out of Ingredients` $\rightarrow$ `Cancelled`, lưu lý do và kích hoạt hoàn tiền $\rightarrow$ **PASS**

---

## 5.2 Deployment

### Môi trường thực thi yêu cầu
- **.NET SDK 8.0 / 10.0** (đã kiểm thử thành công trên `.NET 10.0.401`).
- **Hệ quản trị CSDL quan hệ:** MySQL 8.0+ hoặc MariaDB (chạy `schema.sql` và `seed.sql`); ứng dụng C# `SaigonBite.csproj` sử dụng tầng DAO trong bộ nhớ (`In-Memory Storage`) giúp chạy demo độc lập không cần cấu hình server DB cục bộ.
- **Trình duyệt web hiện đại** (Chrome / Edge) để chạy trực tiếp giao diện nguyên mẫu `Part_3/ui_prototype/UC7_KDS_Prototype.html`.

### Các bước cài đặt và vận hành demo
1. **Nạp CSDL quan hệ (tùy chọn khi kết nối MySQL):**
   ```sql
   SOURCE Part_3/database/schema.sql;
   SOURCE Part_3/database/seed.sql;
   ```
2. **Biên dịch và chạy ứng dụng C# 3 lớp (Live Run):**
   ```powershell
   dotnet run --project Part_3/src/csharp/SaigonBite.csproj
   ```
3. **Mở giao diện KDS Prototype cho UC7:** Mở file `Part_3/ui_prototype/UC7_KDS_Prototype.html` bằng trình duyệt để thao tác trực tiếp Confirm / Reject đơn hàng với đồng hồ đếm ngược 120 giây.
