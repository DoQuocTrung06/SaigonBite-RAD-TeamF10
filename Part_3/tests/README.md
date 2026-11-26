# HƯỚNG DẪN KẾ HOẠCH & KỊCH BẢN KIỂM THỬ (TEST CASES) (PART 3)
**Thư mục lưu trữ:** `Part_3/tests/`  
**Người phụ trách chính:** Nguyễn Quang Tựu (`524H0136`) tổng hợp  
**Người hỗ trợ:** Đỗ Quốc Trung (`524H0132`), Ngô Tấn Thành (`524H0031`)  

---

## 1. Yêu Cầu Của Giảng Viên (Mục 5.1 & Rubric Tiêu Chí 4)

- Các Test Cases **bắt buộc phải được rút ra trực tiếp từ các Post-conditions** trong Đặc tả Use Case (Fully Developed Use Case Descriptions).
- Cấu trúc chuẩn của một Test Case bao gồm các cột sau:
  1. **Test Case ID:** Mã kiểm thử (ví dụ: `TC_UC10_01`, `TC_UC10_02`).
  2. **Use Case Name:** Tên Use Case tương ứng.
  3. **Derived Post-condition:** Trạng thái hệ thống sau khi thực thi thành công hoặc thất bại theo đặc tả.
  4. **Test Description:** Mô tả ngắn gọn tình huống kiểm thử (Normal flow hoặc Exception flow).
  5. **Pre-conditions / Input Data:** Dữ liệu đầu vào cần thiết để chạy test.
  6. **Expected Output:** Kết quả mong đợi (Trạng thái đơn, dữ liệu trong CSDL, thông báo trên giao diện).
  7. **Actual Result:** Kết quả thực tế quan sát được khi chạy phần mềm.
  8. **Status:** Đánh giá `PASS` hoặc `FAIL`.

---

## 2. Danh Mục Test Cases Tối Thiểu Cần Có

Mỗi thành viên phụ trách xây dựng ít nhất **2 - 3 Test Cases** cho từng Use Case sở hữu:

- **Đỗ Quốc Trung (`524H0132`):**
  - `TC_UC15_01`: Tạo voucher hợp lệ, kiểm tra quota và hạn sử dụng được lưu trữ vào CSDL.
  - `TC_UC7_01`: Bếp xác nhận đơn hàng trong 120s -> Trạng thái đổi thành `Confirmed`.
  - `TC_UC7_02`: Bếp từ chối đơn hàng do hết món -> Trạng thái đổi thành `Cancelled` kèm lý do, kích hoạt refund.
- **Ngô Tấn Thành (`524H0031`):**
  - `TC_UC14_01`: Thêm món mới vào menu thành công với giá VND dương (> 0).
  - `TC_UC3_01`: Đặt đơn hàng thành công trong bán kính 7km -> Tính đúng phí ship, trừ quota voucher, lưu vào DB.
  - `TC_UC3_02`: Đặt đơn hàng vượt quá bán kính 7km -> Hệ thống từ chối và hiển thị thông báo lỗi.
- **Nguyễn Quang Tựu (`524H0136`):**
  - `TC_UC10_01`: Giao hàng thành công -> Cập nhật trạng thái `Delivered`, thu COD, cộng tiền ví Shipper.
  - `TC_UC10_02`: Khách không nhận sau 10 phút đếm ngược -> Cập nhật trạng thái `Delivery_Failed`, ghi lý do hoàn hàng về Hub.
  - `TC_UC16_01`: Xuất báo cáo doanh thu theo thương hiệu và tỷ lệ tuân thủ SLA của Shipper trong khoảng ngày tùy chọn.

---

## 3. Các File Cần Bàn Giao Trong Thư Mục Này

- `test_cases_matrix.xlsx` (hoặc chèn trực tiếp vào sheet `Test Cases` trong `TeamF10_RAD_Team_Workbook.xlsx`).
- `test_results_summary.md`: Bản tổng kết kết quả kiểm thử toàn diện của hệ thống để đưa vào Mục 5.1 của Báo cáo BRS/SRS.
