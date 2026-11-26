# KẾ HOẠCH CÔNG VIỆC PART 3 — NGUYỄN QUANG TỰU (524H0136)
**Họ và tên:** Nguyễn Quang Tựu  
**Mã sinh viên:** `524H0136`  
**Vai trò nhóm:** Logistics & Reporting Lead  
**2 Use Cases sở hữu:** UC10 (*Deliver an order*), UC16 (*Produce management reports*)  
**Use Case chọn làm Video cá nhân:** **UC10: Deliver an order**  

---

## 1. Nhiệm Vụ Thuyết Trình Cá Nhân (Individual Video Presentation — 30 Điểm)

Bạn quay **01 video cá nhân (< 15 phút)** trình bày chi tiết về **UC10: Deliver an order**. Video được chấm theo 6 tiêu chí của Rubric:

| Tiêu chí Rubric | Điểm tối đa | Yêu cầu chi tiết cần trình bày trong Video UC10 |
| :--- | :---: | :--- |
| **P3: Analysis Model** | **6.0 đ** | - Trình bày **Activity Diagram** của UC10 (quét QR lấy hàng tại Hub, định vị GPS drop-off, gọi khách đếm ngược 10 phút, thu COD).<br>- Trình bày **System Sequence Diagram (SSD)** của UC10.<br>- Đọc & phân tích **Đặc tả Use Case** (Pre-conditions và Post-conditions).<br>- Chỉ rõ mối liên hệ giữa Post-condition với **State Machine Diagram** của `DeliveryTask`/`Order` (chuyển trạng thái từ `Out_for_Delivery` -> `Delivered` hoặc `Delivery_Failed`).<br>- Trình bày các lớp liên quan trong **Domain Model Class Diagram** (`Shipper`, `DeliveryTask`, `Order`, `Payment`). |
| **P3: Design Model** | **6.0 đ** | - Trình bày **First-Cut Design Class Diagram** của UC10.<br>- Trình bày **CRC Cards** phân định trách nhiệm các lớp 3 tầng.<br>- Trình bày **3-Layer Sequence Diagram** của UC10 (ShipperView -> DeliveryController -> DeliveryTask & Order -> DeliveryRepository).<br>- Trình bày **Final Design Class Diagram** hoàn chỉnh với đầy đủ phương thức và kiểu dữ liệu. |
| **P3: User Interface** | **5.0 đ** | - Chiếu bản vẽ **Prototype UI (Figma/Canva)** màn hình Mobile App của Shipper.<br>- Chỉ rõ các màn hình: Quét mã QR nhận kiện hàng tại Hub, Bản đồ dẫn đường GPS tới địa chỉ khách hàng, Nút gọi khách hàng có **đồng hồ đếm ngược 10 phút** khi khách không bắt máy, Màn hình xác nhận thu tiền mặt COD và hoàn tất chuyến giao.<br>- **Quan trọng:** Giải thích rõ từng bước thông điệp trong SSD được chuyển hóa thành các thành phần giao diện UI tương ứng. |
| **P3: Test Cases** | **4.0 đ** | - Trình bày ít nhất 2 Test Cases được sinh trực tiếp từ Post-conditions của UC10:<br>  + **TC1 (Giao hàng thành công & Thu COD):** Input = Shipper ấn xác nhận giao thành công, nhập số tiền COD thu được -> Expected = Đơn hàng chuyển trạng thái `Delivered`, cập nhật số dư ví tài xế Shipper, ghi nhận thời gian hoàn tất.<br>  + **TC2 (Khách hàng không nhận sau 10 phút):** Input = Đếm ngược hết 10 phút khách không nghe máy, ấn báo giao thất bại -> Expected = Đơn hàng chuyển trạng thái `Delivery_Failed`, ghi lý do "Customer unreachable after 10m", tạo lệnh hoàn trả gói hàng về Hub.<br>- Trình bày bảng Test Case gồm: Test ID, Input, Expected Result, Actual Result, Status Pass/Fail. |
| **P3: Programming Model** | **6.0 đ** | - Mở mã nguồn source code (các Class `DeliveryController`, `DeliveryTask`, `Shipper`, `DeliveryRepository`).<br>- Chiếu các bảng CSDL liên quan trong Database (`delivery_tasks`, `orders`, `shippers`).<br>- **Chạy demo trực tiếp (Live Run):** Thao tác gọi hàm cập nhật trạng thái `updateDeliveryStatus()`, xác nhận thu COD và xem dữ liệu cập nhật trực tiếp trong CSDL. |
| **P3: Video & Transcript** | **3.0 đ** | - Video quay màn hình rõ nét, âm thanh rõ ràng, thời lượng **dưới 15 phút**.<br>- Kèm file kịch bản lời thoại **Transcript** (`Transcript_524H0136_UC10.docx` hoặc `.pdf`). |

---

## 2. Nhiệm Vụ Phần Chung Của Nhóm (Team Deliverables)

Với vai trò Logistics & Reporting Lead, bạn phụ trách các nội dung sau cho Báo cáo chung:
1. **Tổng hợp Design Classes (Mục 4.1 Design Classes for the Subsystem):**
   - Lập bảng tổng hợp toàn bộ các lớp thiết kế 3 tầng (View, Controller, Domain Entity, Data Access) của cả 6 Use Cases.
2. **Sơ đồ Package Diagram (Mục 4.2 Package Diagram for the Subsystem):**
   - Thiết kế sơ đồ UML Package Diagram thể hiện kiến trúc 3 tầng phân rã rõ ràng:
     - Tầng View/Presentation Layer
     - Tầng Controller/Application Layer
     - Tầng Domain/Business Logic Layer
     - Tầng Data Access/Persistence Layer
3. **Kịch bản tích hợp hệ thống (Mục 4.3.6 Integration of Use Cases):**
   - Viết kịch bản liên kết luồng hoạt động xuyên suốt 6 Use Cases thành 1 chu trình vận hành khép kín (Admin cấu hình Voucher & Menu -> Khách đặt món -> Bếp nhận đơn -> Shipper giao hàng -> Quản lý xem báo cáo doanh thu & SLA).
4. **Soạn thảo Test Cases cho UC10 & UC16 (Mục 5.1):**
   - Viết các bảng Test Cases chi tiết rút ra từ Post-conditions của UC10 (*Deliver an order*) và UC16 (*Produce management reports*).
   - Tổng hợp toàn bộ Test Cases của cả nhóm vào Báo cáo và file Excel `TeamF10_RAD_Team_Workbook.xlsx`.
5. **Hoàn thiện Phần Kết luận (Conclusions & Recommendations) và References:**
   - Đánh giá khách quan kết quả đạt được, hạn chế của hệ thống SaigonBite và đề xuất hướng phát triển tương lai.
   - Định dạng danh mục tài liệu tham khảo theo chuẩn IEEE.

---

## 3. Sản Phẩm Cần Nộp Trong Thư Mục Này

- [ ] File Slide thuyết trình cá nhân: `Presentation_524H0136_UC10.pptx`
- [ ] File Kịch bản lời thoại: `Transcript_524H0136_UC10.docx` (hoặc `.pdf`)
- [ ] Video thuyết trình: `TeamF10_Project_for_SaigonBite_524H0136.mp4` (hoặc link Google Drive nếu file nặng)
- [ ] Source code hoàn thiện của UC10 & UC16 (đẩy vào `Part_3/src/`)
- [ ] Sơ đồ Package Diagram (đẩy vào thư mục `Part_3/docs/` hoặc Báo cáo)
