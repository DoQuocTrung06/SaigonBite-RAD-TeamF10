# TỔNG QUAN PART 3 (SPRINT 2 - FINAL SUBMISSION)
**Môn học:** Phân tích và Thiết kế Yêu cầu (PTTKYC / RAD) — Học kỳ Sem01_2627  
**Dự án:** SaigonBite – Nền tảng Cloud Kitchen & Đặt món đa thương hiệu (OFDH)  
**Nhóm:** Team F10 | **Hạn nộp:** 30/11/2026  

---

## 1. Cơ Cấu Điểm & Các Thành Phần Cần Nộp Cho Part 3

Theo **Marking Sheet chính thức** (`RAD_Sem01_2627_MarkingSheet.xlsx`), Part 3 bao gồm hai phần chính:

| STT | Thành phần nộp | Trọng số | Mô tả chi tiết |
| :---: | :--- | :---: | :--- |
| **1** | **Báo cáo chung BRS/SRS (Hoàn thiện Phần IV & V)** | **17.5 điểm** *(trong Part 2)* | Hoàn thiện nốt **Mục IV: System Requirements Implementation (10đ)**, **Mục V: System Testing, Deployment & Demonstration (7.5đ)**, và phần **Conclusions/Recommendations** trong file Word & PDF. |
| **2** | **Thuyết trình cá nhân (Individual Video Presentation)** | **30 điểm / SV** | Mỗi thành viên tự quay **1 video (< 15 phút)** trình bày sâu **1 Use Case chính** của mình, chấm theo 6 tiêu chí: Phân tích (6đ), Thiết kế (6đ), UI Prototype (5đ), Test Case (4đ), Code demo chạy thật (6đ), Video & Transcript (3đ). |
| **3** | **Sổ tay dự án & Bảng tự chấm điểm** | **Bắt buộc** | Cập nhật `TeamF10_RAD_Team_Workbook.xlsx` (Sprint 2 Log, Commit count, Test cases) và điền tự chấm điểm cá nhân ở sheet `Part 3 Individual` trong `TeamF10_Marking_Workbook.xlsx`. |
| **4** | **GitHub Repository & Release** | **Bắt buộc** | Mã nguồn hoàn chỉnh, cấu trúc rõ ràng, mỗi thành viên phải có **> 10 commits**, gắn release tag `v1.0-final-part3`. |

---

## 2. Cấu Trúc Thư Mục Trong `Part_3/`

```text
Part_3/
├── README.md                      # File tổng quan hướng dẫn chung cho Part 3 (File này)
├── Trung_524H0132/                # Thư mục công việc cá nhân của Đỗ Quốc Trung
│   └── README.md                  # Hướng dẫn chi tiết công việc, video UC7 & rubric 30đ
├── Thanh_524H0031/                # Thư mục công việc cá nhân của Ngô Tấn Thành
│   └── README.md                  # Hướng dẫn chi tiết công việc, video UC3 & rubric 30đ
├── Tuu_524H0136/                  # Thư mục công việc cá nhân của Nguyễn Quang Tựu
│   └── README.md                  # Hướng dẫn chi tiết công việc, video UC10 & rubric 30đ
├── database/                      # CSDL quan hệ: Schema, Seed data, ERD
│   └── README.md
├── ui_prototype/                  # Thiết kế giao diện UI: Link Figma, Wireframes, SSD mapping
│   └── README.md
├── src/                           # Mã nguồn hướng đối tượng (OOP) chạy thật
│   └── README.md
└── tests/                         # Bảng kế hoạch & kịch bản kiểm thử (Test Cases)
    └── README.md
```

---

## 3. Bảng Phân Chia Use Case Thuyết Trình Cá Nhân (30 Điểm / Thành Viên)

| Thành viên | MSSV | Vai trò | 2 Use Cases sở hữu | Use Case chọn làm Video cá nhân |
| :--- | :---: | :---: | :---: | :---: |
| **Đỗ Quốc Trung** | `524H0132` | Project Manager & Architect | UC15, UC7 | **UC7: Confirm or reject an incoming order** |
| **Ngô Tấn Thành** | `524H0031` | Analysis & UI Lead | UC14, UC3 | **UC3: Place an order** |
| **Nguyễn Quang Tựu** | `524H0136` | Logistics & Reporting Lead | UC10, UC16 | **UC10: Deliver an order** |

---

## 4. Danh Mục Bàn Giao Chung Cho Báo Cáo (Section IV & V)

- **Mục 4.1 Design Classes:** Tổng hợp danh mục các lớp 3 tầng (View, Controller, Domain, Data Access) – *Tựu phụ trách*.
- **Mục 4.2 Package Diagram:** Sơ đồ UML Package kiến trúc 3 tầng – *Tựu phụ trách*.
- **Mục 4.3.1 Relational DB Mapping:** Ánh xạ từ Domain Model sang Bảng CSDL (ERD/Relational Schema) – *Trung phụ trách*.
- **Mục 4.3.2 Modifying Sequence Diagrams:** Bổ sung tầng Data Access vào Sequence Diagram – *Cả 3 thành viên làm cho UC của mình*.
- **Mục 4.3.3 UI Design:** Bộ giao diện UI hoàn chỉnh trên Figma/Canva đối chiếu từng message từ SSD – *Thành dựng khung, cả nhóm hoàn thiện*.
- **Mục 4.3.4 SQL Code:** Script SQL (`schema.sql` và `seed.sql`) – *Trung phụ trách*.
- **Mục 4.3.5 Software Classes & Code:** Mã nguồn OOP (Models, Controllers, Repositories) – *Cả 3 thành viên code cho các UC tương ứng*.
- **Mục 4.3.6 Integration of Use Cases:** Kịch bản luồng tích hợp xuyên suốt 6 use cases – *Tựu phụ trách*.
- **Mục 5.1 Test Plan & Test Cases:** Bảng Test cases rút ra từ Post-conditions – *Cả 3 thành viên viết cho UC của mình, Tựu tổng hợp*.
- **Mục 5.2 Deployment & 5.3 Demo:** Hướng dẫn cài đặt, môi trường runtime và kịch bản demo hệ thống – *Trung & Tựu phụ trách*.
- **Conclusions / Recommendations & References:** Tổng kết hạn chế, giải pháp và danh mục tham khảo IEEE – *Tựu phụ trách*.

---

## 5. Quy Chuẩn Đặt Tên File Nộp Bài (Checklist Mục 38 & 52)

- Báo cáo BRS/SRS: `TeamF10_BRS_SRS_for_SaigonBite.pdf` và `TeamF10_BRS_SRS_for_SaigonBite.docx`
- Slide thuyết trình chung: `TeamF10_Presentation_for_SaigonBite.pptx`
- Video cá nhân từng thành viên: `TeamF10_Project_for_SaigonBite_524H0132.mp4` (Trung), `_524H0031.mp4` (Thành), `_524H0136.mp4` (Tựu)
- Sổ tay dự án: `TeamF10_RAD_Team_Workbook.xlsx`
- Bảng chấm điểm: `TeamF10_Marking_Workbook.xlsx`
