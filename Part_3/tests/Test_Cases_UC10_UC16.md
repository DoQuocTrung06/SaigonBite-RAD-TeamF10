# BẢNG KẾ HOẠCH & KỊCH BẢN KIỂM THỬ (TEST CASES) CHO UC10 & UC16
**Học phần:** Phân tích và Thiết kế Yêu cầu (RAD Sem01_2627)  
**Nhóm:** Team F10 — SaigonBite Platform  
**Tác giả:** Nguyễn Quang Tựu (MSSV: `524H0136`) — Logistics & Reporting Lead  

---

## 1. Nguyên Tắc Thiết Kế Test Cases

Các Test Cases dưới đây được **sinh trực tiếp từ các Post-conditions** trong bản đặc tả Use Case (Section 2.2):
- **UC10 (Deliver an order):**
  - Post-condition thành công: Trạng thái Order đổi thành `Delivered`, `delivered_at` được ghi nhận, số tiền COD đã thu được lưu vào CSDL, tài xế được cộng tiền công vào ví.
  - Post-condition ngoại lệ: Trạng thái Order đổi thành `Delivery_Failed`, ghi nhận `failure_reason`, tạo mã hoàn kiện hàng về Hub.
- **UC16 (Produce management reports):**
  - Post-condition: Bản ghi `ManagementReport` được tạo, tính đúng tổng doanh thu, tỷ lệ giao hàng đạt SLA và danh sách phân rã theo thương hiệu.

---

## 2. Bảng Ma Trận Test Cases Chi Tiết

| Test Case ID | Use Case & Kịch bản | Post-condition đối chiếu | Dữ liệu đầu vào (Test Input) | Kết quả mong đợi (Expected Output) | Kết quả thực tế (Actual Result) | Đánh giá |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_UC10_01** | **UC10 (Normal Flow):** Giao hàng thành công & Thu đủ tiền mặt COD | Order đổi sang `Delivered`, lưu COD, cộng ví Shipper | - `taskId`: "TASK_01"<br>- `orderId`: "ORD_1001"<br>- `qrToken`: "QR_SGB_ORD1001_VALID"<br>- `amountPaid`: 127,500 VND | - Order status = `Delivered`<br>- Task status = `Delivered`<br>- `cod_collected_vnd` = 127,500<br>- Shipper wallet: 150k -> 170k | Khớp 100% với CSDL và thông báo trên giao diện | **PASS** |
| **TC_UC10_02** | **UC10 (Exception Flow):** Khách không nhận sau đếm ngược 10 phút | Order đổi sang `Delivery_Failed`, ghi nhận lý do hủy | - `taskId`: "TASK_02"<br>- `orderId`: "ORD_1002"<br>- Gọi khách 3 cuộc không nghe<br>- Hết 10 phút timer | - Order status = `Delivery_Failed`<br>- Task status = `Failed_Returned`<br>- `cancellation_reason` = "Customer unreachable after 10m phone calls"<br>- Kiện hàng tạo mã hoàn Hub | Khớp 100% với CSDL và quy trình hoàn hàng | **PASS** |
| **TC_UC10_03** | **UC10 (Exception Flow):** Quét mã QR kiện hàng bị sai mã | Hệ thống từ chối nhận hàng, giữ nguyên trạng thái `Assigned` | - `taskId`: "TASK_01"<br>- `qrToken`: "QR_INVALID_TOKEN_999" | - Báo lỗi "QR code token mismatch!"<br>- Task status vẫn là `Assigned`<br>- Không cho phép xuất phát | Hệ thống từ chối và hiển thị thông báo lỗi chính xác | **PASS** |
| **TC_UC10_04** | **UC10 (Exception Flow):** Thu tiền COD không đủ số lượng | Hệ thống chặn hoàn tất đơn hàng, yêu cầu thu đủ tiền | - `taskId`: "TASK_01"<br>- `amountPaid`: 100,000 VND (thiếu 27,500 VND) | - Báo lỗi "COD amount insufficient!"<br>- Không đổi trạng thái `Delivered`<br>- Không cộng tiền ví tài xế | Hệ thống chặn không cho bấm hoàn tất | **PASS** |
| **TC_UC16_01** | **UC16 (Normal Flow):** Xuất báo cáo doanh thu theo thương hiệu | Tính đúng tổng doanh thu và danh sách doanh thu từng Brand | - `managerId`: "MGR_TUU_01"<br>- `dateFrom`: "2026-11-26"<br>- `dateTo`: "2026-11-26" | - `total_revenue` = 370,000 VND<br>- `total_orders` = 2<br>- Danh sách: Phuc Long (250k), Com Tam (120k) | Báo cáo hiển thị chính xác từng dòng doanh thu | **PASS** |
| **TC_UC16_02** | **UC16 (Normal Flow):** Xuất thống kê tỷ lệ tuân thủ SLA của Shipper | Tính đúng tỷ lệ đơn giao thành công / tổng số đơn được giao | - `managerId`: "MGR_TUU_01"<br>- Khoảng thời gian: ngày hôm nay | - `total_assigned` = 2<br>- `delivered_count` = 1<br>- `failed_count` = 1<br>- `sla_compliance_rate` = 50.0% | Tính đúng 50.0% tỷ lệ SLA | **PASS** |
