# NỘI DUNG ĐÓNG GÓP MỤC IV & MỤC V BÁO CÁO BRS/SRS (PART 3)
**Tác giả:** Nguyễn Quang Tựu (MSSV: `524H0136`) — Logistics & Reporting Lead  
**Đơn vị:** Team F10 — Đồ án Phân tích và Thiết kế Yêu cầu (RAD Sem01_2627)  
**Tài liệu:** Đóng góp trực tiếp cho Báo cáo chính `TeamF10_BRS_SRS_for_SaigonBite.docx`  

---

## 4.1 Design Classes for the Subsystem

Bảng dưới đây tổng hợp danh mục các lớp thiết kế hướng đối tượng được phân bổ theo Kiến trúc 3 tầng (Three-Layer Architecture), phục vụ trực tiếp cho các Use Case thuộc phân hệ Hậu cần Giao hàng (UC10) và Báo cáo Quản trị (UC16) cùng các lớp dùng chung:

| Tầng kiến trúc (Layer) | Tên lớp (Class Name) | Vai trò & Trách nhiệm chính (Responsibilities) | Thuộc tính chính (Attributes) | Phương thức nghiệp vụ chính (Methods) |
| :--- | :--- | :--- | :--- | :--- |
| **View Layer (Boundary)** | `ShipperView` | Giao diện di động cho tài xế: hiển thị camera quét QR, bản đồ GPS, bộ đếm ngược 10 phút, form xác nhận thu tiền COD. | `currentTaskId`, `scannerActive`, `gpsEnabled` | `scanPackageQR()`, `displayNavigationMap()`, `show10MinCountdown()`, `confirmCODCollection()` |
| **View Layer (Boundary)** | `HubManagerView` | Giao diện Web Dashboard cho Quản lý Hub: chọn khoảng ngày, xem biểu đồ doanh thu theo thương hiệu, xuất bảng SLA tài xế. | `selectedDateRange`, `chartType`, `exportFormat` | `selectDateRange()`, `displayRevenueReport()`, `exportSLAStats()` |
| **Controller Layer** | `DeliveryController` | Điều phối luồng nghiệp vụ giao hàng: xác thực mã QR token, cập nhật vị trí GPS, kiểm tra số tiền COD, chuyển trạng thái đơn hàng. | `deliveryRepo: DeliveryRepository` | `scan_package_qr()`, `navigate_to_dropoff()`, `initiate_wait_countdown()`, `confirm_delivery_and_cod()`, `record_delivery_failure()` |
| **Controller Layer** | `ReportController` | Xử lý nghiệp vụ phân tích và tổng hợp dữ liệu điều hành cho cấp quản lý. | `reportRepo: ReportRepository` | `generate_sales_and_sla_report(managerId, dateFrom, dateTo)` |
| **Domain Entity Layer** | `DeliveryTask` | Quản lý vòng đời nhiệm vụ giao hàng, lưu vết thời gian nhận hàng, đến nơi, chờ đợi, và số tiền COD thực thu. | `taskId`, `orderId`, `shipperId`, `qrCodeToken`, `taskStatus`, `codCollectedVnd` | `scan_qr_and_pickup()`, `start_10_min_countdown()`, `confirm_successful_delivery()`, `mark_delivery_failed()` |
| **Domain Entity Layer** | `Order` | Thực thể đơn hàng trung tâm của hệ thống, quản lý tính toàn vẹn trạng thái và doanh thu. | `orderId`, `customerId`, `hubId`, `finalAmount`, `paymentMethod`, `orderStatus` | `transition_to(newStatus, reason)` |
| **Domain Entity Layer** | `Shipper` | Thực thể tài xế giao hàng, lưu thông tin xe, tọa độ GPS thời gian thực và số dư ví công nợ. | `shipperId`, `fullName`, `vehiclePlate`, `currentLat`, `currentLng`, `walletBalance` | `update_location(lat, lng)`, `credit_wallet(amount)`, `debit_wallet(amount)` |
| **Domain Entity Layer** | `ManagementReport` | Bản ghi tổng hợp báo cáo quản trị định kỳ. | `reportId`, `reportType`, `generatedAt`, `dateFrom`, `dateTo`, `metricsSummary` | `to_summary_text()` |
| **Data Access Layer** | `DeliveryRepository` | Thực thi các truy vấn SQL lưu trữ và truy xuất thông tin đơn hàng, nhiệm vụ giao và ví tài xế. | `db: DatabaseConnection` | `get_task_by_id()`, `get_order_by_id()`, `save_task()`, `update_order_status()`, `update_shipper_wallet()` |
| **Data Access Layer** | `ReportRepository` | Thực thi các câu lệnh SQL tổng hợp (`GROUP BY`, `SUM`, `COUNT`) từ bảng bán hàng và nhiệm vụ giao. | `db: DatabaseConnection` | `aggregate_brand_revenue()`, `aggregate_shipper_sla()` |
| **Data Access Layer** | `DatabaseConnection` | Quản lý kết nối Singleton và thực thi ràng buộc toàn vẹn khóa ngoại CSDL. | `dbPath`, `_instance` | `get_instance()`, `get_connection()` |

---

## 4.2 Package Diagram for the Subsystem

### Mô tả kiến trúc phân gói (Package Architecture):
Sơ đồ gói (**Figure 4.2 Package Diagram**) được tổ chức thành 4 Package chính tương ứng với mô hình đa tầng chuẩn công nghiệp:
1. **`View Layer (Presentation)`**: Chứa các lớp Boundary chịu trách nhiệm tương tác trực tiếp với các Actor (`CustomerView`, `KitchenStaffView`, `ShipperView`, `HubManagerView`).
2. **`Controller Layer (Application Logic)`**: Chứa các Controller tiếp nhận yêu cầu từ View, không chứa logic giao diện, giữ vai trò nhạc trưởng điều phối các tương tác nghiệp vụ.
3. **`Domain Layer (Business Entities)`**: Chứa các đối tượng nghiệp vụ cốt lõi phản ánh thế giới thực của nền tảng SaigonBite (`Order`, `DeliveryTask`, `Shipper`, `MenuItem`, `Voucher`). Tầng này độc lập hoàn toàn với tầng giao diện và tầng CSDL.
4. **`Data Access Layer (Persistence & DAO)`**: Đóng gói toàn bộ logic truy vấn SQL (`SELECT`, `INSERT`, `UPDATE`), chuyển đổi giữa các dòng dữ liệu quan hệ (Rows) thành các đối tượng Domain.
5. **Ràng buộc phụ thuộc một chiều (Unidirectional Dependencies):** `View` chỉ phụ thuộc `Controller`; `Controller` phụ thuộc `Domain` và `Data Access`; `Data Access` phụ thuộc `Domain` và `Database`. Tuyệt đối không có phụ thuộc vòng (Circular Dependencies), đảm bảo tính module hóa và dễ bảo trì.

*(Hình ảnh minh họa chèn từ: `Part_3/docs/Figure_4_2_Package_Diagram.png`)*

---

## 4.3.2 Modifying Sequence Diagrams (Bổ sung tầng Data Access cho UC10)

Trong giai đoạn thiết kế cài đặt, Sơ đồ Tuần tự của **UC10 (Deliver an order)** được nâng cấp từ mô hình phân tích sang mô hình thiết kế chi tiết bằng cách thêm sự tham gia của `DeliveryRepository` và cơ sở dữ liệu vật lý `SQLite Database`:
- Khi tài xế gửi thông điệp `scanPackageQR()`, Controller không tự truy cập CSDL mà gọi phương thức `getTaskById()` của Repository. Sau khi thực thể `DeliveryTask` xác thực mã QR thành công, Controller gọi `saveTask()` và `updateOrderStatus()` để phát lệnh SQL `UPDATE delivery_tasks` và `UPDATE orders SET order_status = 'Out_for_Delivery'`.
- Khi đến nơi và hoàn tất giao hàng, thông điệp `confirmDeliveryAndCOD()` kích hoạt một chuỗi giao dịch nguyên tử (Atomic Transaction): (1) Cập nhật trạng thái đơn thành `Delivered`, (2) Ghi nhận số tiền COD đã thu, (3) Thực thi câu lệnh `UPDATE shippers SET wallet_balance = wallet_balance + 20000` để cộng thù lao giao hàng vào ví tài xế.
- Ở kịch bản khách không liên lạc được, lệnh `start10MinTimer()` cập nhật trạng thái `Waiting_Customer_10Min`. Khi hết 10 phút, phương thức `recordDeliveryFailure()` cập nhật trạng thái `Delivery_Failed` kèm lý do vào trường `cancellation_reason`.

*(Hình ảnh minh họa chèn từ: `Part_3/docs/Figure_4_3_2_UC10_Modified_Sequence_Diagram.png`)*

---

## 4.3.6 Integration of Use Cases (Tích hợp luồng chạy 6 Use Cases)

Sáu Use Cases chính của nhóm F10 tạo thành một chu trình vận hành khép kín (Closed-Loop Operational Workflow) của nền tảng Bếp trên mây SaigonBite:
1. **Thiết lập danh mục & Khuyến mãi (UC14 & UC15):** Quản trị viên cấu hình thương hiệu, món ăn (UC14) và tạo mã Voucher kích cầu (UC15). Dữ liệu này được lưu sẵn trong bảng `menu_items` và `vouchers`.
2. **Khách hàng đặt món đa thương hiệu (UC3):** Khách hàng chọn nhiều món từ các thương hiệu khác nhau thuộc cùng một Hub, nhập địa chỉ trong bán kính 7km, áp mã giảm giá và chọn phương thức thanh toán COD hoặc Online Card. Đơn hàng được tạo ở trạng thái `Created`.
3. **Tiếp nhận & Chế biến tại Bếp (UC7):** Màn hình Tablet của Bếp nhận thông báo đơn mới. Bếp trưởng xác nhận trong vòng 120 giây (chuyển sang `Confirmed`) và hệ thống tự động in phiếu xuống các trạm bếp `KitchenStation` (Wok, Fryer, Salad).
4. **Đóng gói & Phân công Shipper:** Khi các trạm hoàn tất, đơn chuyển sang `Ready_for_Pickup` và được gắn mã QR định danh duy nhất.
5. **Giao hàng tận nơi (UC10):** Tài xế quét mã QR nhận gói hàng, chuyển trạng thái sang `Out_for_Delivery`, điều hướng GPS tới khách, đợi tối đa 10 phút nếu khách trễ, thu tiền mặt COD và xác nhận `Delivered`.
6. **Báo cáo điều hành & Tối ưu hóa (UC16):** Cuối ngày, Quản lý Hub truy cập Dashboard để xem tổng doanh thu theo thương hiệu, tỷ lệ vi phạm SLA của tài xế và thời gian chuẩn bị món trung bình của từng trạm bếp, từ đó đưa ra quyết định điều chỉnh vận hành.

---

## 5.1 Test Plan and Test Cases (Bảng Kiểm thử UC10 & UC16)

*(Nội dung đồng bộ từ: `Part_3/tests/Test_Cases_UC10_UC16.md` và Sheet `Test Cases` trong Workbook)*

- `TC_UC10_01`: Giao hàng thành công & Thu đủ tiền COD (Normal Flow) -> **PASS**
- `TC_UC10_02`: Khách hàng không nhận sau 10 phút đếm ngược (Exception Flow) -> **PASS**
- `TC_UC10_03`: Quét sai mã QR kiện hàng tại Hub (Exception Flow) -> **PASS**
- `TC_UC10_04`: Thu thiếu tiền COD (Exception Flow) -> **PASS**
- `TC_UC16_01`: Tổng hợp doanh thu theo từng thương hiệu -> **PASS**
- `TC_UC16_02`: Tính tỷ lệ tuân thủ SLA của đội ngũ Shipper -> **PASS**

---

## Conclusions & Recommendations (Kết luận & Đề xuất phát triển)

### 1. Kết quả đạt được:
- Nhóm đã hoàn thành trọn vẹn chu trình Phân tích và Thiết kế hệ thống thông tin theo phương pháp lặp Iterative UP kết hợp Scrum.
- Toàn bộ các yêu cầu từ ca sử dụng đến thiết kế hướng đối tượng 3 tầng đều được chứng minh tính khả thi thông qua mã nguồn thực thi và cơ sở dữ liệu quan hệ chạy thật.
- Các bài toán nghiệp vụ đặc thù của Cloud Kitchen (đơn hàng đa quán cùng trạm, tính phí ship theo bán kính 7km, phân chia trạm bếp, đếm ngược 10 phút và đối soát COD) được giải quyết triệt để và tường minh.

### 2. Hạn chế còn tồn tại:
- Hệ thống hiện tại mới mô phỏng định vị GPS dựa trên tọa độ điểm (Point-to-Point) chứ chưa tích hợp Google Maps API trả phí thời gian thực để tính toán tắc đường (Traffic Congestion).
- Cơ chế phân phối đơn cho Shipper đang dựa trên thứ tự gán đơn (First-Come First-Served), chưa áp dụng thuật toán tối ưu hóa tuyến đường đa điểm giao (Vehicle Routing Problem - VRP).

### 3. Đề xuất hướng phát triển tương lai:
- Ứng dụng mô hình học máy (Machine Learning) để dự báo nhu cầu đặt món theo khung giờ và thời tiết, giúp Hub chuẩn bị trước nguyên liệu tại các KitchenStation.
- Tích hợp cổng thanh toán trực tuyến qua mã VietQR động để giảm thiểu rủi ro xử lý tiền mặt COD cho tài xế.

---

## References (Tài liệu tham khảo chuẩn IEEE)

- [1] J. W. Satzinger, R. B. Jackson, and S. D. Burd, *Systems Analysis and Design in a Changing World*, 7th ed. Boston, MA, USA: Cengage Learning, 2016.
- [2] Pham Thai Ky Trung, *RAD Final Project Requirements and Case Study: SaigonBite Cloud-Kitchen Delivery Hub (Sem01_2627)*, Faculty of Information Technology, Ton Duc Thang University, Ho Chi Minh City, Vietnam, 2026.
- [3] M. Fowler, *Patterns of Enterprise Application Architecture*, Boston, MA, USA: Addison-Wesley Professional, 2002.
- [4] E. Gamma, R. Helm, R. Johnson, and J. Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software*, Reading, MA, USA: Addison-Wesley, 1994.
