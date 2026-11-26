# HƯỚNG DẪN CSDL & SQL SCRIPTS (PART 3)
**Thư mục lưu trữ:** `Part_3/database/`  
**Người phụ trách chính:** Đỗ Quốc Trung (`524H0132`)  
**Người hỗ trợ:** Nguyễn Quang Tựu (`524H0136`), Ngô Tấn Thành (`524H0031`)  

---

## 1. Yêu Cầu Của Giảng Viên (Mục 4.3.1 & 4.3.4)

File SQL phải chứa đầy đủ 3 phần rõ ràng:
1. **i. Create database**: Lệnh tạo CSDL (ví dụ `CREATE DATABASE IF NOT EXISTS saigonbite_db;`).
2. **ii. Create tables**: Định nghĩa toàn bộ các bảng CSDL tương ứng với Domain Model & Design Class Diagrams:
   - Có đầy đủ kiểu dữ liệu thích hợp (`INT`, `VARCHAR`, `DECIMAL`, `DATETIME`, `BOOLEAN`, `ENUM`).
   - Ràng buộc khóa chính (`PRIMARY KEY`), khóa ngoại (`FOREIGN KEY`) và tính toàn vẹn tham chiếu (`ON DELETE CASCADE` / `RESTRICT`).
   - Ràng buộc kiểm tra nghiệp vụ (`CHECK`): Giá tiền > 0, khoảng cách <= 7.0 km, tải bếp < 85%, số tiền giảm voucher không âm.
3. **iii. Sample data**: Lệnh `INSERT INTO` chứa bộ dữ liệu mẫu hợp lệ cho cả 6 Use Cases (Tài khoản khách, Thương hiệu, Thực đơn, Voucher, Đơn hàng, Kitchen Station, Shipper, Báo cáo).

---

## 2. Danh Mục Các Bảng Cần Tạo

1. `users` & `customers` (kế thừa chuyên biệt hóa: `LocalCustomer` với SĐT Việt Nam 10 số, `ForeignTourist` với Passport/Email quốc tế; trong CSDL quan hệ thiết kế bảng `customers` có `customer_type` ENUM/CHECK ('Local', 'Foreign') khớp 100% Mục 2.1.7 & Feedback Log A-04)
2. `hubs` & `kitchen_stations` (Whole-Part Composition)
3. `brands` & `menu_items` (Quản lý thực đơn ảo đa thương hiệu)
4. `vouchers` (Quản lý mã giảm giá, quota, hạn sử dụng)
5. `orders` & `order_lines` (Association Class lưu chi tiết món, giá, ghi chú)
6. `payments` (COD hoặc Thẻ tín dụng/Online)
7. `shippers` & `delivery_tasks` (Theo dõi nhiệm vụ giao hàng, định vị, trạng thái)
8. `management_reports` (Dữ liệu tổng hợp doanh thu, SLA, tải trạm bếp)

---

## 3. Các File Cần Bàn Giao Trong Thư Mục Này

- `schema.sql`: Script tạo database và cấu trúc các bảng kèm ràng buộc.
- `seed.sql`: Script nạp dữ liệu mẫu ban đầu để chạy demo.
- `saigonbite_erd.png`: Ảnh chụp sơ đồ quan hệ thực thể (ERD/Relational Schema) phục vụ chèn vào báo cáo.
