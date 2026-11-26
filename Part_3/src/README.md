# HƯỚNG DẪN MÃ NGUỒN PHẦN MỀM (OOP SOURCE CODE) (PART 3)
**Thư mục lưu trữ:** `Part_3/src/`  
**Người phụ trách chính:** Cả 3 thành viên phụ trách các lớp nghiệp vụ của mình.  

---

## 1. Yêu Cầu Của Giảng Viên (Mục 4.3.5 & Rubric Tiêu Chí 5)

Mã nguồn phải được tổ chức chuẩn theo **Kiến trúc 3 tầng (Three-Layer Architecture)**, phản ánh chính xác các lớp đã thiết kế trong Final Design Class Diagram (DCD):
- **Tầng View / Presentation (UI / API Endpoints / Console UI)**: Nhận tương tác từ người dùng và gửi yêu cầu tới Controller.
- **Tầng Controller / Application Logic**: Tiếp nhận yêu cầu, phối hợp các đối tượng nghiệp vụ, kiểm tra ràng buộc logic.
- **Tầng Domain / Entity**: Chứa các lớp thực thể nghiệp vụ (`Order`, `OrderItem`, `MenuItem`, `Voucher`, `DeliveryTask`, `Hub`, `KitchenStation`, `Shipper`).
- **Tầng Data Access / Persistence (DAO / Repository)**: Thực hiện các câu lệnh SQL để lưu trữ và truy xuất dữ liệu từ Database.

---

## 2. Cấu Trúc Mã Nguồn Đề Xuất

```text
Part_3/src/
├── main.py (hoặc app.py / App.java / Program.cs)   # Điểm khởi chạy ứng dụng (Entry point)
├── controllers/                                    # Tầng điều khiển (Controllers)
│   ├── voucher_controller.py                      # Trung (UC15)
│   ├── order_confirmation_controller.py           # Trung (UC7)
│   ├── menu_controller.py                         # Thành (UC14)
│   ├── checkout_controller.py                     # Thành (UC3)
│   ├── delivery_controller.py                     # Tựu (UC10)
│   └── report_controller.py                       # Tựu (UC16)
├── models/                                         # Tầng thực thể nghiệp vụ (Domain Entities)
│   ├── customer.py
│   ├── order.py
│   ├── order_item.py
│   ├── menu_item.py
│   ├── voucher.py
│   ├── delivery_task.py
│   ├── hub.py
│   └── kitchen_station.py
├── data_access/                                    # Tầng truy xuất dữ liệu (Repositories / DAO)
│   ├── db_connection.py                           # Quản lý kết nối CSDL
│   ├── order_repository.py
│   ├── menu_repository.py
│   ├── delivery_repository.py
│   └── report_repository.py
└── utils/                                          # Các hàm tiện ích (Validation, Distance, Pricing)
```

---

## 3. Quy Định Commit Trên GitHub (Checklist Mục 39)

- Barem yêu cầu **mỗi sinh viên phải có > 10 commits có ý nghĩa** trên GitHub.
- Khi code từng hàm, class, hoặc sửa bug, các thành viên hãy commit thường xuyên với message rõ ràng, ví dụ:
  - `feat(uc10): implement updateDeliveryStatus and COD collection method (524H0136)`
  - `feat(uc3): implement calculateDeliveryFee and voucher discount validation (524H0031)`
  - `feat(uc7): implement confirmOrder and rejectOrder with cancellation reason (524H0132)`
