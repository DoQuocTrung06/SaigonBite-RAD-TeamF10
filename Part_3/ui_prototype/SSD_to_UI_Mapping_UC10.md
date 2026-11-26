# ĐẶC TẢ GIAO DIỆN UI & BẢNG ÁNH XẠ SSD SANG UI (SSD-TO-UI MAPPING)
**Use Case 10:** Deliver an order (Giao hàng, định vị GPS, đợi 10 phút, thu COD)  
**Tác giả:** Nguyễn Quang Tựu (MSSV: `524H0136`) — Logistics & Reporting Lead  
**Dự án:** SaigonBite – Nền tảng Cloud Kitchen & Đặt món đa thương hiệu  
**Ứng dụng:** SaigonBite Shipper Mobile App (iOS / Android)  

---

## 1. Bảng Ánh Xạ Chi Tiết Giữa Thông Điệp SSD Và Giao Diện UI

Bảng dưới đây chứng minh tính truy vết 100% (Full Traceability) từ các thông điệp trong **System Sequence Diagram (SSD Figure 2.10)** sang các thành phần giao diện thực tế trên ứng dụng di động của Shipper:

| STT | Thông điệp trên SSD (Message Name & Parameters) | Hướng gửi | Màn hình UI tương ứng | Thành phần giao diện (UI Widget / Element) | Mô tả hành vi & Kiểm tra nghiệp vụ |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **1** | `scanPackageQR(taskId, qrToken)` | Shipper -> System | **SCR-01: Hub Package Pickup** | Camera Viewfinder + Nút "Quét mã QR kiện hàng" | Camera tự động nhận diện mã QR in trên tem dán hộp đồ ăn tại Hub. Hệ thống đối chiếu token với `qr_code_token` trong DB. |
| **2** | `pickupConfirmed(orderId, dropoffAddress, distanceKm)` | System -> Shipper | **SCR-01: Hub Package Pickup** | Popup Modal màu xanh lá + Thông tin tóm tắt đơn | Hiển thị: "Xác nhận nhận hàng thành công!", mã đơn hàng `ORD_1001`, địa chỉ drop-off và nút "Bắt đầu điều hướng GPS". |
| **3** | `updateGPSLocation(taskId, lat, lng)` | Shipper -> System | **SCR-02: Live Navigation** | Bản đồ GPS (Map SDK) + Marker vị trí tài xế | Ứng dụng tự động gửi tọa độ GPS định kỳ mỗi 5 giây, vẽ tuyến đường ngắn nhất từ Hub đến vị trí khách. |
| **4** | `navigationRoute(routePolyline, estimatedMins)` | System -> Shipper | **SCR-02: Live Navigation** | Thanh chỉ đường Turn-by-Turn + Thời gian dự kiến | Hiển thị: "Còn 1.2 km (khoảng 6 phút)", chỉ dẫn rẽ trái/phải trên đường Nguyễn Hữu Thọ. |
| **5** | `arriveAtDropoff(taskId)` | Shipper -> System | **SCR-02: Live Navigation** | Nút gạt "Tôi đã đến nơi" (Swipe to Arrive) | Khi tài xế đến cách địa chỉ giao hàng < 50m, nút chuyển màu xanh, tài xế gạt để chuyển sang màn hình giao hàng. |
| **6** | `start10MinTimer(taskId)` | Shipper -> System | **SCR-03: Customer Contact & 10m Wait** | Nút bấm "Khách không nghe máy (Bắt đầu đợi 10p)" | Khi tài xế gọi điện 3 lần không liên lạc được, ấn nút này để kích hoạt đếm ngược 10 phút. |
| **7** | `waitingTimerStarted(remainingSeconds: 600)` | System -> Shipper | **SCR-03: Customer Contact & 10m Wait** | Đồng hồ đếm ngược vòng tròn (Circular Timer 10:00) | Đồng hồ đếm lùi từng giây: `09:59`, `09:58`... Kèm nút gọi lại "Gọi lại cho khách". Nếu khách bắt máy, ấn "Khách đã ra nhận". |
| **8** | `confirmDeliveryAndCOD(taskId, amountPaid)` | Shipper -> System | **SCR-04: Settlement & Completion** | Form nhập số tiền COD thu được + Nút "Xác nhận giao & Thu COD" | Đối với đơn COD: Hiển thị số tiền cần thu e.g. `127,500 VND`. Ô nhập tiền mặt tài xế nhận. Bắt buộc số tiền >= `final_amount`. |
| **9** | `deliveryCompleted(orderStatus, creditedWallet)` | System -> Shipper | **SCR-04: Settlement & Completion** | Màn hình Hoàn tất chuyến giao (Success Screen) | Thông báo: "Đơn hàng hoàn tất!". Cộng tiền công giao hàng (+20,000 VND) vào ví tài xế, hiển thị số dư ví mới. |
| **10** | `recordDeliveryFailure(taskId, failureReason)` | Shipper -> System | **SCR-03: Customer Contact & 10m Wait** | Nút màu đỏ "Xác nhận Giao thất bại" (mở sau khi hết 10p) | Khi đồng hồ đếm về `00:00`, nút này sáng lên. Tài xế ấn xác nhận hủy đơn, chọn lý do "Khách không nghe máy sau 10p". Hệ thống tạo mã hoàn hàng về Hub. |

---

## 2. Mô Tả Chi Tiết 4 Màn Hình Giao Diện Shipper Mobile App

```text
+-----------------------------+  +-----------------------------+
| SCR-01: HUB PICKUP & QR     |  | SCR-02: GPS NAVIGATION      |
| [SaigonBite Shipper]        |  | [SaigonBite Navigation]     |
| Task: TASK_01               |  | Don hang: ORD_1001          |
| Hub: District 7 Central Hub |  | Khach: Nguyen Van A         |
| +-------------------------+ |  | Dia chi: 19 Nguyen Huu Tho  |
| |                         | |  | +-------------------------+ |
| |   [ SCAN CAMERA QR ]    | |  | |  [ MAP: HUB -> DROP ]   | |
| |                         | |  | |    Shipper Marker (GPS) | |
| +-------------------------+ |  | +-------------------------+ |
| Ma don: ORD_1001            |  | Con: 1.2 km (5 phut)        |
| [ NUT: XAC NHAN QUET QR ]   |  | [ GAT: TOI DA DEN NOI ]     |
+-----------------------------+  +-----------------------------+

+-----------------------------+  +-----------------------------+
| SCR-03: 10-MIN COUNTDOWN    |  | SCR-04: COD & COMPLETION    |
| [Lien he khach hang]        |  | [Xac nhan thu tien COD]     |
| Goi dien khach khong nghe!  |  | Ma don: ORD_1001            |
|       +-------------+       |  | Phuong thuc: TIEN MAT (COD) |
|      /   10:00       \      |  | --------------------------- |
|     |  DANG DEM LUI   |     |  | So tien can thu: 127,500 đ  |
|      \   09:42       /      |  | Tien thuc thu:  [127,500 đ] |
|       +-------------+       |  | Chu ky khach hang: [Sign Pad|
| [ NUT: GOI LAI CHO KHACH ]  |  | --------------------------- |
| [ NUT: KHACH DA RA NHAN ]   |  | Tien cong cong vi: +20,000 đ|
| (Het 10p: Xac nhan huy don) |  | [ NUT: XAC NHAN HOAN TAT ]  |
+-----------------------------+  +-----------------------------+
```

---

## 3. Quy Tắc Chống Lỗi Giao Diện & Trải Nghiệm Người Dùng (UX Rules)

1. **Khóa nút thu COD khi chưa nhận đủ tiền:** Nút "Xác nhận hoàn tất" bị vô hiệu hóa (disabled) nếu ô số tiền thực thu nhỏ hơn số tiền trên đơn hàng.
2. **Bảo vệ đếm ngược 10 phút:** Khi màn hình đếm ngược đang chạy, tài xế không thể vô tình bấm hủy đơn; nút "Giao thất bại" chỉ mở khóa khi đồng hồ đếm về đúng `00:00`.
3. **Chế độ Ngoại tuyến tạm thời:** Nếu mất sóng GPS tạm thời, app lưu tọa độ cuối cùng và gửi bù ngay khi có kết nối trở lại.
