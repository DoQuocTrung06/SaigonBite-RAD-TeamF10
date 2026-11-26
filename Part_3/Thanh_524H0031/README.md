# KẾ HOẠCH CÔNG VIỆC PART 3 — NGÔ TẤN THÀNH (524H0031)
**Họ và tên:** Ngô Tấn Thành  
**Mã sinh viên:** `524H0031`  
**Vai trò nhóm:** Analysis & UI Lead  
**2 Use Cases sở hữu:** UC14 (*Manage brands and menu items*), UC3 (*Place an order*)  
**Use Case chọn làm Video cá nhân:** **UC3: Place an order**  

---

## 1. Nhiệm Vụ Thuyết Trình Cá Nhân (Individual Video Presentation — 30 Điểm)

Bạn quay **01 video cá nhân (< 15 phút)** trình bày chi tiết về **UC3: Place an order**. Video được chấm theo 6 tiêu chí của Rubric:

| Tiêu chí Rubric | Điểm tối đa | Yêu cầu chi tiết cần trình bày trong Video UC3 |
| :--- | :---: | :--- |
| **P3: Analysis Model** | **6.0 đ** | - Trình bày **Activity Diagram** của UC3 (chọn món đa thương hiệu cùng Hub, kiểm tra bán kính 7km, tính phí ship, áp voucher, thanh toán).<br>- Trình bày **System Sequence Diagram (SSD)** của UC3.<br>- Đọc & phân tích **Đặc tả Use Case** (Pre-conditions và Post-conditions).<br>- Chỉ rõ mối liên hệ giữa Post-condition với **State Machine Diagram** của Order (tạo order mới chuyển sang trạng thái `Pending_Kitchen`).<br>- Trình bày các lớp liên quan trong **Domain Model Class Diagram** (`Customer`, `Cart`, `Order`, `OrderLine`, `MenuItem`, `Voucher`). |
| **P3: Design Model** | **6.0 đ** | - Trình bày **First-Cut Design Class Diagram** của UC3 (Hình 3.5).<br>- Trình bày **CRC Cards** phân định trách nhiệm các lớp 3 tầng (Bảng 21 & 22 trong Báo cáo).<br>- Trình bày **3-Layer Sequence Diagram** của UC3 (Hình 3.6): `CheckoutWindow` -> `OrderHandler` -> `Customer` (`LocalCustomer`/`ForeignTourist`), `Hub`, `Order`, `OrderLine`, `MenuItem`, `Voucher` -> `OrderDA`, `HubDA`, `VoucherDA`. Giải thích rõ Sequence Part 1 (Cart & Pricing) và Part 2 (Payment & Checkout).<br>- Trình bày **Final Design Class Diagram** (Hình 3.7) hoàn chỉnh với đầy đủ phương thức và kiểu dữ liệu. |
| **P3: User Interface** | **5.0 đ** | - Chiếu bản vẽ **Prototype UI (Figma/Canva)** màn hình `CheckoutWindow` trên Mobile App của Khách hàng.<br>- Chỉ rõ các màn hình: Duyệt thực đơn đa thương hiệu cùng Hub, Giỏ hàng kết hợp, Màn hình thanh toán (nhập địa chỉ, hiển thị phí giao hàng 15k/2km + 5k/km, ô nhập voucher), Chọn phương thức COD / Online Card.<br>- **Quan trọng:** Giải thích rõ từng bước thông điệp trong SSD được chuyển hóa thành các thành phần giao diện UI tương ứng. |
| **P3: Test Cases** | **4.0 đ** | - Trình bày ít nhất 2 Test Cases được sinh trực tiếp từ Post-conditions của UC3 (Khớp Test T-01 & T-02 trong Báo cáo & Workbook):<br>  + **TC1 (Đặt hàng thành công):** Input = Đơn hàng hợp lệ trong 7km, áp voucher hợp lệ -> Expected = Đơn hàng được tạo với mã Order ID, trạng thái `Placed`/`Pending_Kitchen`, trừ quota voucher.<br>  + **TC2 (Địa chỉ vượt bán kính 7km):** Input = Địa chỉ cách Hub 8.5km -> Expected = Hệ thống từ chối checkout, báo lỗi ngoài vùng phục vụ.<br>- Trình bày bảng Test Case gồm: Test ID, Input, Expected Result, Actual Result, Status Pass/Fail. |
| **P3: Programming Model** | **6.0 đ** | - Mở mã nguồn source code đúng chuẩn tên lớp trong Final DCD Hình 3.7:<br>  + View: `CheckoutWindow`<br>  + Controller: `OrderHandler`<br>  + Domain Entities: `Customer` (`LocalCustomer`, `ForeignTourist`), `Hub`, `Order`, `OrderLine`, `MenuItem`, `Voucher`, `Payment`<br>  + Data Access: `OrderDA`, `HubDA`, `VoucherDA`, `MenuItemDA`<br>- Chiếu các bảng CSDL liên quan trong Database (`orders`, `order_lines`, `vouchers`, `menu_items`, `customers`).<br>- **Chạy demo trực tiếp (Live Run):** Thao tác tính giá giỏ hàng, áp voucher, và tạo đơn hàng hiển thị trong CSDL. |
| **P3: Video & Transcript** | **3.0 đ** | - Video quay màn hình rõ nét, âm thanh rõ ràng, thời lượng **dưới 15 phút**.<br>- Kèm file kịch bản lời thoại **Transcript** (`Transcript_524H0031_UC3.docx` hoặc `.pdf`). |

---

## 2. Nhiệm Vụ Phần Chung Của Nhóm (Team Deliverables)

Với vai trò Analysis & UI Lead, bạn phụ trách các nội dung sau cho Báo cáo chung:
1. **Thiết kế UI Prototype hệ thống (Mục 4.3.3 UI Design):**
   - Dựng khung bộ giao diện UI Prototype hoàn chỉnh trên Figma / Canva.
   - Thể hiện sự nhất quán về phong cách thiết kế, font chữ, màu sắc thương hiệu SaigonBite.
   - Cung cấp link Figma hoặc xuất ảnh chụp màn hình độ phân giải cao để chèn vào báo cáo.
2. **Soạn thảo Test Cases cho UC14 & UC3 (Mục 5.1 Test Plan & Test Cases):**
   - Viết các bảng Test Cases chi tiết rút ra từ Post-conditions của UC14 (*Manage brands and menu items*) và UC3 (*Place an order*).
3. **Mã nguồn chức năng UC14 & UC3 (Mục 4.3.5):**
   - Hoàn thiện mã nguồn Model, Controller cho việc quản lý thực đơn (UC14) và tạo đơn hàng (UC3), đưa vào thư mục `Part_3/src/`.

---

## 3. Sản Phẩm Cần Nộp Trong Thư Mục Này

- [ ] File Slide thuyết trình cá nhân: `Presentation_524H0031_UC3.pptx`
- [ ] File Kịch bản lời thoại: `Transcript_524H0031_UC3.docx` (hoặc `.pdf`)
- [ ] Video thuyết trình: `TeamF10_Project_for_SaigonBite_524H0031.mp4` (hoặc link Google Drive nếu file nặng)
- [ ] Source code hoàn thiện của UC14 & UC3 (đẩy vào `Part_3/src/`)
- [ ] Link Figma UI Prototype và ảnh chụp màn hình (đẩy vào `Part_3/ui_prototype/`)
