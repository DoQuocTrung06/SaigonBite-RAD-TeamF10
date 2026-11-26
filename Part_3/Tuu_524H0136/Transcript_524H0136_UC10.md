# KỊCH BẢN THUYẾT TRÌNH VIDEO CÁ NHÂN (PART 3 TRANSCRIPT)
**Môn học:** Phân tích và Thiết kế Yêu cầu (PTTKYC / RAD) — Sem01_2627  
**Dự án:** SaigonBite – Nền tảng Cloud Kitchen & Đặt món đa thương hiệu  
**Sinh viên thuyết trình:** Nguyễn Quang Tựu (MSSV: `524H0136`)  
**Vai trò:** Logistics & Reporting Lead — Team F10  
**Use Case báo cáo:** `UC10: Deliver an order` (Giao hàng, định vị GPS, đợi 10 phút, thu COD)  
**Thời lượng dự kiến:** 10 – 12 phút (Đảm bảo dưới 15 phút theo quy định)  

---

## [00:00 - 01:00] SLIDE 1: GIỚI THIỆU MỞ ĐẦU
*(Mở đầu slide tiêu đề, giọng nói tự tin, rõ ràng)*

> "Kính chào Thầy và các bạn!  
> Em tên là **Nguyễn Quang Tựu**, mã số sinh viên **524H0136**, là thành viên phụ trách mảng Logistics & Reporting Lead thuộc Nhóm F10 môn Phân tích và Thiết kế Yêu cầu (RAD).  
> 
> Hôm nay, em xin phép được trình bày bài báo cáo thuyết trình cá nhân cho **Part 3 (Sprint 2 - Final Submission)** về Use Case mà em trực tiếp đảm nhận thiết kế và triển khai: **Use Case 10: Deliver an order (Giao hàng)** trong nền tảng giao đồ ăn đa thương hiệu SaigonBite.  
> 
> Use Case này có độ phức tạp cao và mang tính thực tiễn đặc thù của mô hình bếp trung tâm Cloud Kitchen, bao gồm luồng nhận kiện hàng bằng mã QR tại Hub, điều hướng GPS tới điểm giao khách, xử lý ngoại lệ đếm ngược 10 phút khi khách không liên lạc được, và quy trình thu nộp tiền mặt COD."

---

## [01:00 - 02:00] SLIDE 2: MỤC TIÊU BÁO CÁO & BAREM ĐIỂM PART 3 (30 ĐIỂM)
*(Chuyển sang Slide 2 - Agenda)*

> "Bài thuyết trình hôm nay của em được xây dựng bám sát 100% theo 6 tiêu chí đánh giá trong Bảng chấm điểm chính thức của Giảng viên với tổng điểm 30 điểm tối đa:  
> 1. **Analysis Model (6.0 điểm):** Phân tích quy trình nghiệp vụ qua Activity Diagram, SSD, Pre/Post-conditions gắn liền với State Machine Diagram và Domain Model.  
> 2. **Design Model (6.0 điểm):** Thiết kế hướng đối tượng 3 tầng (Three-Layer Architecture) gồm First-Cut & Final DCD, CRC Cards và Multilayer Sequence Diagram.  
> 3. **User Interface (5.0 điểm):** Bản mẫu Prototype di động cho Shipper trên Figma, thể hiện tính truy vết 1-1 từ thông điệp SSD sang các widget giao diện.  
> 4. **Test Cases (4.0 điểm):** Bộ kịch bản kiểm thử rút ra trực tiếp từ các Post-conditions.  
> 5. **Programming Model (6.0 điểm):** Cấu trúc mã nguồn OOP chạy thật và demo trực tiếp trên màn hình kết nối CSDL SQLite.  
> 6. **Presentation & Transcript (3.0 điểm):** Kỹ năng truyền đạt chuyên nghiệp, đúng thời lượng và có kịch bản đồng bộ."

---

## [02:00 - 03:30] SLIDE 3: ANALYSIS MODEL — ACTIVITY DIAGRAM & PRE/POST CONDITIONS (6 ĐIỂM)
*(Chuyển sang Slide 3 - Activity Diagram & Đặc tả)*

> "Đầu tiên, về **Analysis Model**:  
> Use Case 10 được kích hoạt khi đơn hàng đã được trạm bếp đóng gói hoàn tất và chuyển sang trạng thái `Ready_for_Pickup`.  
> - **Tiền điều kiện (Pre-conditions):** Tài xế Shipper đã đăng nhập vào hệ thống, đang ở trạng thái sẵn sàng nhận chuyến; kiện hàng đã được dán nhãn mã QR duy nhất tại trạm đóng gói của Hub.  
> - **Luồng sự kiện chính trên Activity Diagram:**  
>   + Tài xế đến Hub, dùng ứng dụng quét mã QR kiện hàng. Hệ thống xác thực mã thành công và chuyển trạng thái đơn hàng sang `Out_for_Delivery`.  
>   + Tài xế xuất phát, ứng dụng liên tục gửi tọa độ GPS về máy chủ để cập nhật lộ trình.  
>   + Khi đến địa chỉ khách hàng, tài xế giao món và thu tiền mặt COD. Sau khi nhận đủ tiền, tài xế bấm xác nhận trên app.  
> - **Hậu điều kiện thành công (Post-conditions - Normal Flow):** Đơn hàng và nhiệm vụ giao hàng chuyển trạng thái `Delivered`, hệ thống ghi nhận thời điểm hoàn tất, lưu số tiền COD thu được và lập tức cộng tiền công giao hàng (+20,000 VND) vào ví tài xế.  
> - **Hậu điều kiện ngoại lệ (Exception Flow - 10 Min Timeout):** Nếu đến nơi gọi điện khách không bắt máy sau 3 cuộc, tài xế kích hoạt đồng hồ đếm ngược 10 phút. Hết 10 phút khách vẫn không ra nhận, đơn hàng chuyển trạng thái `Delivery_Failed`, ghi nhận lý do và tạo phiếu hoàn trả kiện hàng về Hub."

---

## [03:30 - 04:30] SLIDE 4: ANALYSIS MODEL — SSD & STATE MACHINE LINKAGE
*(Chuyển sang Slide 4 - SSD và State Machine)*

> "Trên màn hình là **System Sequence Diagram (SSD)** hộp đen và **State Machine Diagram** của thực thể `Order` và `DeliveryTask`.  
> Em xin nhấn mạnh tính liên kết chặt chẽ giữa thông điệp SSD và sự chuyển đổi trạng thái:  
> - Khi thông điệp `scanPackageQR()` được gửi thành công, `DeliveryTask` chuyển từ `Assigned` sang `Picked_Up`, đồng thời `Order` chuyển từ `Ready_for_Pickup` sang `Out_for_Delivery`.  
> - Khi tài xế đến nơi và kích hoạt `start10MinTimer()`, task chuyển sang trạng thái chờ `Waiting_Customer_10Min`.  
> - Cuối cùng, thông điệp `confirmDeliveryAndCOD()` đưa trạng thái đơn hàng về trạng thái kết thúc `Delivered`. Ngược lại, nếu hết thời gian chờ, thông điệp `recordDeliveryFailure()` sẽ chuyển trạng thái đơn hàng sang `Delivery_Failed`.  
> Điều này đảm bảo tính nhất quán tuyệt đối giữa mô hình động và mô hình hành vi của hệ thống."

---

## [04:30 - 05:45] SLIDE 5: DESIGN MODEL — THREE-LAYER ARCHITECTURE & DCD (6 ĐIỂM)
*(Chuyển sang Slide 5 - 3-Layer Design Class Diagram)*

> "Bước sang giai đoạn **Design Model**:  
> Hệ thống được thiết kế tuân thủ nghiêm ngặt nguyên lý **Kiến trúc 3 tầng (Three-Layer Architecture)** nhằm tách biệt giao diện, nghiệp vụ và lưu trữ:  
> 1. **Tầng View (Boundary):** Lớp `ShipperView` đảm nhận giao tiếp di động, hiển thị camera quét QR, hiển thị bản đồ và form nhập tiền COD.  
> 2. **Tầng Controller:** Lớp `DeliveryController` điều phối toàn bộ luồng nghiệp vụ giao hàng, xác thực mã QR token, kiểm tra số tiền COD và gọi hàm cập nhật trạng thái.  
> 3. **Tầng Domain Entity:** Gồm thực thể `DeliveryTask`, `Order`, và `Shipper` chứa các thuộc tính nghiệp vụ và các phương thức chuyển trạng thái như `scanQRAndPickup()`, `confirmSuccessfulDelivery()`, `creditWallet()`.  
> 4. **Tầng Data Access:** Lớp `DeliveryRepository` và `DatabaseConnection` chịu trách nhiệm thực thi các truy vấn SQL xuống cơ sở dữ liệu SQLite/MySQL, che giấu hoàn toàn chi tiết kỹ thuật lưu trữ khỏi tầng Domain."

---

## [05:45 - 07:00] SLIDE 6: DESIGN MODEL — MULTILAYER SEQUENCE DIAGRAM
*(Chuyển sang Slide 6 - Modified Sequence Diagram)*

> "Trên Slide 6 là **Sơ đồ Tuần tự Thiết kế chi tiết (Design Sequence Diagram)** có tích hợp đầy đủ tầng CSDL.  
> Luồng xử lý được chia làm 3 pha rất rõ ràng:  
> - **Pha 1: Quét QR tại Hub.** ShipperView gửi yêu cầu tới DeliveryController. Controller gọi Repository lấy dữ liệu `delivery_tasks`, gọi thực thể `DeliveryTask` để kiểm tra token, sau đó lưu lại trạng thái `Picked_Up` và cập nhật đơn hàng thành `Out_for_Delivery` bằng lệnh SQL `UPDATE`.  
> - **Pha 2: Điều hướng GPS.** Tọa độ tài xế được gửi định kỳ, cập nhật vị trí hiện tại và thời điểm đến địa chỉ drop-off.  
> - **Pha 3: Khung rẽ nhánh (Alt Frame).**  
>   + Ở nhánh Normal: Shipper xác nhận thu COD, Controller kiểm tra số tiền khách trả đủ 127,500 VND thì gọi Repository cập nhật trạng thái `Delivered`, đồng thời thực thi lệnh `UPDATE shippers SET wallet_balance = wallet_balance + 20000` để cộng thưởng cho tài xế.  
>   + Ở nhánh Exception: Khi khách không liên lạc được, hệ thống kích hoạt bộ đếm 10 phút. Hết giờ, Controller gọi hàm ghi nhận `Delivery_Failed` kèm lý do và đóng phiên giao."

---

## [07:00 - 08:15] SLIDE 7: USER INTERFACE — SHIPPER MOBILE PROTOTYPE (5 ĐIỂM)
*(Chuyển sang Slide 7 - 4 Màn hình UI)*

> "Về khía cạnh **User Interface (Giao diện người dùng)**:  
> Em đã thiết kế 4 màn hình trọng tâm cho ứng dụng di động SaigonBite Shipper:  
> 1. **Màn hình SCR-01 (Hub QR Pickup):** Tích hợp khung ngắm camera quét mã QR trên nhãn đơn hàng tại trạm Hub. Nút 'Xác nhận quét QR' tương ứng trực tiếp với thông điệp `scanPackageQR()` trên SSD.  
> 2. **Màn hình SCR-02 (GPS Navigation):** Tích hợp bản đồ trực quan, thanh chỉ đường Turn-by-Turn và nút gạt 'Tôi đã đến nơi' tương ứng với thông điệp `arriveAtDropoff()`.  
> 3. **Màn hình SCR-03 (10m Wait Countdown):** Khi gọi điện khách không nghe máy, màn hình xuất hiện đồng hồ đếm ngược vòng tròn đỏ `10:00` chạy lùi từng giây. Nút 'Giao thất bại' bị khóa trong suốt 10 phút và chỉ mở khi đồng hồ chạm `00:00`, giúp tránh việc tài xế hủy đơn sai quy trình.  
> 4. **Màn hình SCR-04 (COD & Completion):** Hiển thị rõ số tiền cần thu 127,500 VND, ô nhập tiền thực thu, khung ký tên điện tử của khách và nút 'Hoàn tất giao & Thu COD'. Khi bấm hoàn tất, màn hình hiển thị ngay thông báo thù lao +20,000 VND được cộng vào ví tài xế."

---

## [08:15 - 09:15] SLIDE 8: TEST CASES — SINH TỪ POST-CONDITIONS (4 ĐIỂM)
*(Chuyển sang Slide 8 - Bảng Test Cases)*

> "Tiếp theo là phần **Kiểm thử (Test Cases)**:  
> Toàn bộ các Test Cases đều được rút ra trực tiếp từ các Post-conditions của Use Case:  
> - **TC_UC10_01 (Kịch bản chính):** Kiểm tra giao hàng thành công và thu đủ tiền COD. Dữ liệu đầu vào: Mã đơn `ORD_1001`, tiền thu 127,500 VND. Kết quả mong đợi: Đơn đổi trạng thái `Delivered`, số dư ví tài xế tăng từ 150,000 lên 170,000 VND. Kết quả thực tế: Đạt [PASS] 100%.  
> - **TC_UC10_02 (Kịch bản ngoại lệ 10 phút):** Kiểm tra khi hết thời gian chờ 10 phút. Kết quả mong đợi: Đơn đổi thành `Delivery_Failed`, ghi nhận lý do 'Customer unreachable after 10m', tạo mã hoàn về Hub. Kết quả thực tế: Đạt [PASS] 100%.  
> - **TC_UC10_03 (Ngoại lệ mã QR):** Kiểm tra khi quét mã QR sai lệch hoặc bị rách. Kết quả mong đợi: Hệ thống quăng lỗi `ValueError`, từ chối xuất phát và giữ nguyên trạng thái `Assigned`. Kết quả thực tế: Đạt [PASS] 100%."

---

## [09:15 - 11:00] SLIDE 9 & 10: PROGRAMMING MODEL & LIVE DEMONSTRATION (6 ĐIỂM)
*(Chuyển sang Slide 9 & 10, mở terminal chạy demo)*

> "Sau đây, em xin phép trình bày phần **Programming Model** và **Chạy demo trực tiếp (Live Run)** mã nguồn chương trình:  
> Toàn bộ mã nguồn được xây dựng bằng Python hướng đối tượng, phân chia thư mục rõ ràng theo đúng 3 tầng: `models/`, `controllers/` và `data_access/`, kết nối CSDL SQLite quan hệ có đầy đủ các ràng buộc khóa chính, khóa ngoại và ràng buộc CHECK khoảng cách <= 7km.  
> 
> Bây giờ em xin phép thực thi script demo trực tiếp `demo_uc10_delivery.py`:  
> *(Thao tác gõ lệnh: `python Part_3/Tuu_524H0136/demo_uc10_delivery.py` trên màn hình)*  
> 
> Như Thầy có thể quan sát trên màn hình console:  
> - Ở **Kịch bản 1**: Hệ thống khởi tạo tài xế Nguyễn Quang Tựu với số dư ví 150,000 VND. Sau khi quét mã QR `QR_SGB_ORD1001_VALID`, đơn hàng chuyển sang `Out_for_Delivery`. Khi tài xế xác nhận thu đủ 127,500 VND, trạng thái trong CSDL lập tức đổi thành `Delivered`, và ví tài xế được cộng thêm đúng 20,000 VND thành 170,000 VND.  
> - Ở **Kịch bản 2**: Đơn hàng `ORD_1002` sau khi xuất phát gặp tình huống khách không nghe máy, kích hoạt đồng hồ đếm ngược `Waiting_Customer_10Min`. Khi xác nhận giao thất bại, hệ thống tự động ghi nhận lý do vào CSDL và chuyển trạng thái `Delivery_Failed`.  
> - Hệ thống còn tích hợp xuất báo cáo quản trị **UC16** tổng hợp doanh thu theo từng Brand và tỷ lệ SLA của Shipper một cách tự động.  
> Cả 2 kịch bản đều vượt qua kiểm thử thành công 100%."

---

## [11:00 - 12:00] SLIDE 11 & 12: TỔNG KẾT & KẾT THÚC BÁO CÁO
*(Chuyển sang Slide 11 - Summary và Slide 12 - Q&A)*

> "Tổng kết lại, trong Part 3 này, em đã hoàn thành trọn vẹn:  
> - Đảm bảo tính liên kết xuyên suốt 100% từ Mô hình phân tích -> Mô hình thiết kế 3 tầng -> Bản vẽ giao diện UI -> Mã nguồn OOP chạy thật kết nối CSDL.  
> - Giải quyết triệt để các bài toán nghiệp vụ thực tế như tính khoảng cách, đối soát tiền mặt COD và xử lý ngoại lệ đếm ngược 10 phút.  
> - Tự đánh giá mức độ hoàn thành đạt **30.0 / 30.0 điểm tối đa** theo đúng barem điểm cá nhân của Giảng viên.  
> 
> Em xin chân thành cảm ơn Thầy đã lắng nghe bài thuyết trình của em! Em rất mong nhận được những góp ý quý báu của Thầy để hoàn thiện sản phẩm tốt hơn nữa. Em xin trân trọng cảm ơn!"
