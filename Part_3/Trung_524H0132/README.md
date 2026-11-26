# KẾ HOẠCH CÔNG VIỆC PART 3 — ĐỖ QUỐC TRUNG (524H0132)
**Họ và tên:** Đỗ Quốc Trung  
**Mã sinh viên:** `524H0132`  
**Vai trò nhóm:** Project Manager & Architect  
**2 Use Cases sở hữu:** UC15 (*Manage vouchers*), UC7 (*Confirm or reject an incoming order*)  
**Use Case chọn làm Video cá nhân:** **UC7: Confirm or reject an incoming order**  

---

## 1. Nhiệm Vụ Thuyết Trình Cá Nhân (Individual Video Presentation — 30 Điểm)

Bạn quay **01 video cá nhân (< 15 phút)** trình bày chi tiết về **UC7: Confirm or reject an incoming order**. Video được chấm theo 6 tiêu chí của Rubric:

| Tiêu chí Rubric | Điểm tối đa | Yêu cầu chi tiết cần trình bày trong Video UC7 |
| :--- | :---: | :--- |
| **P3: Analysis Model** | **6.0 đ** | - Trình bày **Activity Diagram** của UC7 (luồng bếp duyệt/từ chối đơn trong 120s).<br>- Trình bày **System Sequence Diagram (SSD)** của UC7.<br>- Đọc & phân tích **Đặc tả Use Case** (Pre-conditions và Post-conditions).<br>- Chỉ rõ mối liên hệ giữa Post-condition với **State Machine Diagram** của Order (chuyển trạng thái từ `Pending_Kitchen` -> `Confirmed` hoặc `Cancelled`).<br>- Trình bày các lớp liên quan trong **Domain Model Class Diagram** (`Order`, `KitchenStation`, `Staff`). |
| **P3: Design Model** | **6.0 đ** | - Trình bày **First-Cut Design Class Diagram** của UC7 (Hình 3.4a).<br>- Trình bày **CRC Cards** phân định trách nhiệm các lớp 3 tầng (Bảng 20 trong Báo cáo).<br>- Trình bày **3-Layer Sequence Diagram** của UC7 (Hình 3.4b): `KDSConsoleUI` -> `KitchenController` -> `Order` & `KitchenTicket` -> `OrderDAO`, `KitchenTicketDAO`, `AuditLogDAO`.<br>- Trình bày **Final Design Class Diagram** (Hình 3.4c) hoàn chỉnh với đầy đủ phương thức và kiểu dữ liệu. |
| **P3: User Interface** | **5.0 đ** | - Chiếu bản vẽ **Prototype UI (Figma/Canva)** màn hình `KDSConsoleUI` (Kitchen Display System trên Tablet/Touchscreen của Bếp).<br>- Chỉ rõ cơ chế: đồng hồ đếm ngược 120 giây (`stop120sTimer`), danh sách món cần làm chia theo trạm `KitchenStation` (Wok, Fryer, Salad...), kiểm tra ngưỡng tải 85% (`Busy`), nút **Confirm** và nút **Reject**.<br>- Popup nhập lý do từ chối khi ấn Reject.<br>- **Quan trọng:** Giải thích rõ từng bước thông điệp trong SSD được chuyển hóa thành các thành phần giao diện UI tương ứng. |
| **P3: Test Cases** | **4.0 đ** | - Trình bày ít nhất 2 Test Cases được sinh trực tiếp từ Post-conditions của UC7 (Khớp Test T-06 trong Báo cáo & Workbook):<br>  + **TC1 (Xác nhận thành công):** Input = Bếp trưởng ấn Confirm đơn hàng trong 120s -> Expected = Trạng thái đơn đổi thành `Confirmed`, khóa địa chỉ giao hàng, in/chia vé `KitchenTicket` xuống các trạm bếp.<br>  + **TC2 (Từ chối đơn hàng):** Input = Đơn hàng bị từ chối kèm lý do bắt buộc (ví dụ: "Hết nguyên liệu") -> Expected = Trạng thái đổi thành `Cancelled` / `Rejected`, kích hoạt hoàn tiền tự động.<br>- Trình bày bảng Test Case gồm: Test ID, Input, Expected Result, Actual Result, Status Pass/Fail. |
| **P3: Programming Model** | **6.0 đ** | - Mở mã nguồn source code đúng chuẩn tên lớp trong Final DCD Hình 3.4c:<br>  + View: `KDSConsoleUI`<br>  + Controller: `KitchenController`<br>  + Domain Entities: `Order`, `KitchenTicket`<br>  + Data Access: `OrderDAO`, `KitchenTicketDAO`, `AuditLogDAO`<br>- Chiếu các bảng CSDL liên quan trong Database (`orders`, `kitchen_tickets`, `kitchen_stations`, `audit_logs`).<br>- **Chạy demo trực tiếp (Live Run):** Thao tác gọi hàm hoặc qua giao diện để thấy đơn hàng chuyển trạng thái trong Database. |
| **P3: Video & Transcript** | **3.0 đ** | - Video quay màn hình rõ nét, âm thanh rõ ràng, thời lượng **dưới 15 phút**.<br>- Kèm file kịch bản lời thoại **Transcript** (`Transcript_524H0132_UC7.docx` hoặc `.pdf`). |

---

## 2. Nhiệm Vụ Phần Chung Của Nhóm (Team Deliverables)

Với vai trò Project Manager & Architect, bạn phụ trách các nội dung sau cho Báo cáo chung:
1. **Thiết kế CSDL quan hệ (Mục 4.3.1 Relational DB Mapping):**
   - Viết phần thuyết minh ánh xạ từ Domain Model sang lược đồ quan hệ Relational Schema.
   - Nêu rõ các quy tắc ánh xạ: Kế thừa Customer (Single Table hoặc Table-per-type), quan hệ Composition Hub - KitchenStation, quan hệ nhiều-nhiều qua Association Class `OrderLine`.
2. **Soạn thảo Script SQL (Mục 4.3.4 SQL Code):**
   - Đặt file tại `Part_3/database/schema.sql` (chứa lệnh `CREATE DATABASE`, `CREATE TABLE` có đầy đủ ràng buộc PK, FK, CHECK).
   - Đặt file tại `Part_3/database/seed.sql` (chứa dữ liệu mẫu `INSERT INTO` hợp lệ cho cả 6 Use Cases).
3. **Kế hoạch triển khai (Mục 5.2 Deployment):**
   - Viết các bước hướng dẫn cài đặt môi trường runtime, import DB và cấu hình chạy hệ thống.
4. **Quản trị GitHub:**
   - Review và merge Pull Requests từ các thành viên.
   - Gắn Tag Release chính thức: `v1.0-final-part3`.

---

## 3. Sản Phẩm Cần Nộp Trong Thư Mục Này

- [ ] File Slide thuyết trình cá nhân: `Presentation_524H0132_UC7.pptx`
- [ ] File Kịch bản lời thoại: `Transcript_524H0132_UC7.docx` (hoặc `.pdf`)
- [ ] Video thuyết trình: `TeamF10_Project_for_SaigonBite_524H0132.mp4` (hoặc link Google Drive nếu file nặng)
- [ ] Source code hoàn thiện của UC15 & UC7 (đẩy vào `Part_3/src/`)
- [ ] File SQL hoàn chỉnh (đẩy vào `Part_3/database/`)
