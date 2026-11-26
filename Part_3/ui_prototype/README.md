# HƯỚNG DẪN UI PROTOTYPE & WIREFRAMES (PART 3)
**Thư mục lưu trữ:** `Part_3/ui_prototype/`  
**Người phụ trách chính:** Ngô Tấn Thành (`524H0031`)  
**Người hỗ trợ:** Đỗ Quốc Trung (`524H0132`), Nguyễn Quang Tựu (`524H0136`)  

---

## 1. Yêu Cầu Của Giảng Viên (Mục 4.3.3 & Rubric Tiêu Chí 3)

- Thiết kế bộ giao diện mẫu hoàn chỉnh từ phác thảo (Sketch/Wireframe) đến bản mẫu tương tác cao (High-Fidelity Prototype) trên **Figma** (hoặc Canva/Balsamiq).
- **Yêu cầu cốt lõi:** Phải thể hiện được **sự chuyển hóa trực tiếp từ System Sequence Diagram (SSD) sang các màn hình và nút bấm UI (SSD-to-UI Mapping)**:
  - Mỗi input message từ Actor trên SSD -> trở thành Form nhập liệu, Text field, hoặc Button trên màn hình UI.
  - Mỗi return message từ System trên SSD -> trở thành Màn hình kết quả, Notification, Toast message, hoặc Bảng danh sách trên UI.

---

## 2. Danh Mục Màn Hình Cần Thiết Kế

1. **Khách hàng (Customer Mobile App - UC3):**
   - Màn hình chọn Hub & duyệt thực đơn đa thương hiệu cùng Hub.
   - Màn hình Giỏ hàng kết hợp nhiều thương hiệu trong 1 Hub.
   - Màn hình Thanh toán (Checkout): Nhập địa chỉ, hiển thị phí ship 15k/2km + 5k/km, ô nhập voucher, chọn hình thức COD/Online.
2. **Nhân viên Bếp (Kitchen Console / Tablet - UC7):**
   - Màn hình tiếp nhận đơn mới với đồng hồ đếm ngược 120 giây.
   - Màn hình chia luồng món ăn theo từng KitchenStation.
   - Nút xác nhận đơn (`Confirm`) và nút từ chối đơn (`Reject`) kèm popup nhập lý do.
3. **Tài xế giao hàng (Shipper Mobile App - UC10):**
   - Màn hình quét mã QR nhận kiện hàng tại Hub.
   - Màn hình bản đồ dẫn đường GPS tới địa chỉ giao hàng.
   - Nút gọi khách hàng kèm đồng hồ đếm ngược 10 phút.
   - Màn hình xác nhận thu tiền mặt COD và hoàn tất chuyến giao.
4. **Quản trị viên & Quản lý Hub (Web Admin Dashboard - UC14, UC15, UC16):**
   - Màn hình cấu hình Voucher & Khuyến mãi (UC15).
   - Màn hình quản lý Thương hiệu & Món ăn (UC14).
   - Màn hình Báo cáo Quản trị: Doanh thu theo thương hiệu, SLA giao hàng của Shipper, Tải trạm bếp (UC16).

---

## 3. Các File Cần Bàn Giao Trong Thư Mục Này

- `FIGMA_LINK.md`: Chứa đường link trực tiếp đến file Figma Project tương tác.
- `screenshots/`: Thư mục chứa ảnh chụp độ phân giải cao của các màn hình chính để chèn vào báo cáo và slide thuyết trình.
- `SSD_to_UI_Mapping.md`: Bảng đối chiếu chi tiết giữa các thông điệp SSD và các thành phần giao diện UI tương ứng.
