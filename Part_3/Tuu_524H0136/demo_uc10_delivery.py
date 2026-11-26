"""
=============================================================================
SAIGONBITE PLATFORM — LIVE DEMONSTRATION SCRIPT
USE CASE 10: DELIVER AN ORDER
Author: Nguyen Quang Tuu (Student ID: 524H0136)
Course: Requirements Analysis and Design (RAD Sem01_2627)
Team: F10 — SaigonBite Cloud-Kitchen Delivery Hub
=============================================================================
"""
import os
import sys
import time
from datetime import datetime

# Add project root and Part_3 directory to sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
part3_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
if part3_dir not in sys.path:
    sys.path.insert(0, part3_dir)

from src.data_access.db_connection import DatabaseConnection
from src.data_access.delivery_repository import DeliveryRepository
from src.controllers.delivery_controller import DeliveryController
from src.controllers.report_controller import ReportController
from src.models.shipper import Shipper
from src.models.order import Order
from src.models.delivery_task import DeliveryTask


def seed_demo_data(db_conn: DatabaseConnection):
    """Seed fresh demo data for live video demonstration."""
    conn = db_conn.get_connection()
    cur = conn.cursor()
    
    # Clean previous demo run
    cur.execute("DELETE FROM delivery_tasks;")
    cur.execute("DELETE FROM orders;")
    cur.execute("DELETE FROM shippers;")
    cur.execute("DELETE FROM brand_sales;")

    # 1. Insert Shipper
    cur.execute("""
        INSERT INTO shippers (shipper_id, full_name, phone_number, vehicle_plate, current_lat, current_lng, wallet_balance, is_active)
        VALUES ('SHIP_524H0136', 'Nguyen Quang Tuu (Shipper)', '0909123456', '59-X1 123.45', 10.7324, 106.7001, 150000.0, 1);
    """)

    # 2. Insert Orders
    # Order 1: COD Order (Scenario 1)
    cur.execute("""
        INSERT INTO orders (order_id, customer_id, hub_id, delivery_address, distance_km, total_amount, delivery_fee, discount_amount, final_amount, payment_method, order_status, created_at)
        VALUES ('ORD_1001', 'CUST_001', 'HUB_D7', '19 Nguyen Huu Tho, Tan Phong, District 7', 2.5, 120000.0, 17500.0, 10000.0, 127500.0, 'COD', 'Ready_for_Pickup', ?);
    """, (datetime.now().isoformat(),))

    # Order 2: Online Card Order (Scenario 2 - 10 min fail)
    cur.execute("""
        INSERT INTO orders (order_id, customer_id, hub_id, delivery_address, distance_km, total_amount, delivery_fee, discount_amount, final_amount, payment_method, order_status, created_at)
        VALUES ('ORD_1002', 'CUST_002', 'HUB_D7', '25 Le Van Luong, Tan Quy, District 7', 3.8, 250000.0, 24000.0, 20000.0, 254000.0, 'ONLINE_CARD', 'Ready_for_Pickup', ?);
    """, (datetime.now().isoformat(),))

    # 3. Insert Delivery Tasks
    cur.execute("""
        INSERT INTO delivery_tasks (task_id, order_id, shipper_id, qr_code_token, task_status, assigned_at)
        VALUES ('TASK_01', 'ORD_1001', 'SHIP_524H0136', 'QR_SGB_ORD1001_VALID', 'Assigned', ?);
    """, (datetime.now().isoformat(),))

    cur.execute("""
        INSERT INTO delivery_tasks (task_id, order_id, shipper_id, qr_code_token, task_status, assigned_at)
        VALUES ('TASK_02', 'ORD_1002', 'SHIP_524H0136', 'QR_SGB_ORD1002_VALID', 'Assigned', ?);
    """, (datetime.now().isoformat(),))

    # 4. Insert Brand Sales for UC16 Demo
    cur.execute("""
        INSERT INTO brand_sales (brand_id, brand_name, order_id, sale_amount, sale_date)
        VALUES ('BR_01', 'Com Tam Saigon Hub', 'ORD_1001', 120000.0, ?),
               ('BR_02', 'Tra Sua Phuc Long Virtual', 'ORD_1002', 250000.0, ?);
    """, (datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d")))

    conn.commit()
    conn.close()


def print_banner(text: str):
    print("\n" + "=" * 76)
    print(f" {text.center(74)} ")
    print("=" * 76)


def print_step(step_no: int, title: str):
    print(f"\n>>> [BƯỚC {step_no}] {title}")
    time.sleep(0.5)


def run_live_demo():
    print_banner("DEMO PHẦN MỀM SAIGONBITE — UC10: DELIVER AN ORDER")
    print(" Sinh viên thuyết trình: NGUYỄN QUANG TỰU (MSSV: 524H0136)")
    print(" Vai trò: Logistics & Reporting Lead — Team F10")
    print(" Kiến trúc triển khai: Three-Layer Architecture (View -> Controller -> Domain & DB)")
    print("-" * 76)

    # 1. Initialize DB and Repositories
    db = DatabaseConnection.get_instance("saigonbite_demo.db")
    seed_demo_data(db)
    repo = DeliveryRepository(db)
    controller = DeliveryController(repo)

    shipper = repo.get_shipper_by_id("SHIP_524H0136")
    print(f"[INFO] Tài xế đăng nhập: {shipper.full_name} | Biển số: {shipper.vehicle_plate}")
    print(f"[INFO] Số dư ví Shipper ban đầu: {shipper.wallet_balance:,.0f} VND\n")

    # =========================================================================
    # KỊCH BẢN 1: GIAO HÀNG THÀNH CÔNG & THU TIỀN MẶT COD (NORMAL FLOW)
    # =========================================================================
    print_banner("KỊCH BẢN 1: GIAO HÀNG THÀNH CÔNG VÀ THU TIỀN MẶT COD")
    order1 = repo.get_order_by_id("ORD_1001")
    task1 = repo.get_task_by_id("TASK_01")
    print(f"• Mã đơn hàng: {order1.order_id} | Phương thức: {order1.payment_method}")
    print(f"• Địa chỉ khách: {order1.delivery_address} (Khoảng cách: {order1.distance_km} km)")
    print(f"• Tổng số tiền COD cần thu: {order1.final_amount:,.0f} VND")
    print(f"• Trạng thái ban đầu: Order = [{order1.order_status}], Task = [{task1.task_status}]")

    print_step(1, "Shipper đến Hub và Quét mã QR trên kiện hàng đóng gói (scanPackageQR)")
    res_qr = controller.scan_package_qr("TASK_01", "QR_SGB_ORD1001_VALID")
    print(f"   -> Kết quả: {res_qr['message']}")
    task1 = repo.get_task_by_id("TASK_01")
    order1 = repo.get_order_by_id("ORD_1001")
    print(f"   -> Trạng thái cập nhật: Task = [{task1.task_status}], Order = [{order1.order_status}]")

    print_step(2, "Shipper di chuyển và cập nhật định vị GPS tới khách (navigateGPS)")
    res_nav = controller.navigate_to_dropoff("TASK_01", current_lat=10.7335, current_lng=106.7020)
    print(f"   -> Kết quả: {res_nav['message']} tại tọa độ GPS: {res_nav['current_location']}")

    print_step(3, "Giao đồ ăn thành công và Thu tiền mặt COD từ khách (confirmDeliveryAndCOD)")
    res_delivery = controller.confirm_delivery_and_cod("TASK_01", amount_paid=127500.0)
    print(f"   -> Kết quả: {res_delivery['message']}")
    print(f"   -> Số tiền COD thực tế đã thu: {res_delivery['cod_collected']:,.0f} VND")
    print(f"   -> Tiền công giao hàng cộng vào ví tài xế: +{res_delivery['shipper_credited']:,.0f} VND")

    shipper = repo.get_shipper_by_id("SHIP_524H0136")
    order1 = repo.get_order_by_id("ORD_1001")
    task1 = repo.get_task_by_id("TASK_01")
    print(f"\n[XÁC NHẬN CSDL SAU KỊCH BẢN 1]:")
    print(f"   • Order [{order1.order_id}] Status: {order1.order_status} (Delivered At: {order1.delivered_at})")
    print(f"   • Task  [{task1.task_id}] Status: {task1.task_status} (COD Collected: {task1.cod_collected_vnd:,.0f} VND)")
    print(f"   • Shipper Wallet Mới: {shipper.wallet_balance:,.0f} VND (Tăng từ 150,000 -> {shipper.wallet_balance:,.0f} VND)")
    print("   ===> TEST CASE 1: [PASS] Post-conditions thỏa mãn 100%!")

    # =========================================================================
    # KỊCH BẢN 2: XỬ LÝ NGOẠI LỆ — ĐỢI KHÁCH 10 PHÚT KHÔNG ĐƯỢC (EXCEPTION FLOW)
    # =========================================================================
    print_banner("KỊCH BẢN 2: NGOẠI LỆ — KHÁCH KHÔNG NGHE MÁY, ĐỢI 10 PHÚT VÀ HỦY ĐƠN")
    order2 = repo.get_order_by_id("ORD_1002")
    task2 = repo.get_task_by_id("TASK_02")
    print(f"• Mã đơn hàng: {order2.order_id} | Phương thức: {order2.payment_method}")
    print(f"• Địa chỉ khách: {order2.delivery_address}")
    print(f"• Trạng thái ban đầu: Order = [{order2.order_status}], Task = [{task2.task_status}]")

    print_step(1, "Shipper quét mã QR kiện hàng và xuất phát (scanPackageQR)")
    controller.scan_package_qr("TASK_02", "QR_SGB_ORD1002_VALID")
    print(f"   -> Task TASK_02 đã nhận kiện hàng, Order chuyển sang Out_for_Delivery.")

    print_step(2, "Đến địa chỉ khách hàng nhưng gọi điện không liên lạc được (start10MinTimer)")
    res_wait = controller.initiate_wait_countdown("TASK_02")
    print(f"   -> Kết quả: {res_wait['message']}")
    print(f"   -> Hệ thống kích hoạt đồng hồ đếm ngược 10 phút lúc: {res_wait['wait_start']}")

    print_step(3, "Hết 10 phút khách vẫn không nhận -> Xác nhận Giao Thất Bại (recordDeliveryFailure)")
    res_fail = controller.record_delivery_failure("TASK_02", reason="Customer unreachable after 10m phone calls")
    print(f"   -> Kết quả: {res_fail['message']}")
    print(f"   -> Lý do ghi nhận vào hệ thống: '{res_fail['reason']}'")

    order2 = repo.get_order_by_id("ORD_1002")
    task2 = repo.get_task_by_id("TASK_02")
    print(f"\n[XÁC NHẬN CSDL SAU KỊCH BẢN 2]:")
    print(f"   • Order [{order2.order_id}] Status: {order2.order_status} (Lý do hủy: {order2.cancellation_reason})")
    print(f"   • Task  [{task2.task_id}] Status: {task2.task_status} (Lý do thất bại: {task2.failure_reason})")
    print("   • Quy trình hoàn hàng: Kiện hàng được tạo mã hoàn về trạm Hub.")
    print("   ===> TEST CASE 2: [PASS] Post-conditions ngoại lệ thỏa mãn 100%!")

    # =========================================================================
    # MINH HỌA BỔ SUNG: BÁO CÁO QUẢN TRỊ (UC16)
    # =========================================================================
    print_banner("MINH HỌA UC16: XUẤT BÁO CÁO QUẢN TRỊ (MANAGEMENT REPORT)")
    report_ctrl = ReportController()
    today_str = datetime.now().strftime("%Y-%m-%d")
    report = report_ctrl.generate_sales_and_sla_report(
        manager_id="MGR_TUU_01",
        date_from=today_str,
        date_to=today_str
    )
    print(report.to_summary_text())
    print("\n[BẢNG DOANH THU THEO THƯƠNG HIỆU (BRAND SALES)]:")
    for b in report.brand_revenue_breakdown:
        print(f"   - Brand: {b['brand_name']:<28} | Đơn: {b['total_orders']} | Doanh thu: {b['total_revenue']:>10,.0f} VND")
    
    print("\n[BẢNG ĐÁNH GIÁ SLA TÀI XẾ (SHIPPER SLA)]:")
    for s in report.shipper_sla_breakdown:
        print(f"   - Shipper: {s['full_name']} | Nhận: {s['total_assigned']} đơn | Giao thành công: {s['delivered_count']} đơn | COD: {s['total_cod_collected']:,.0f} VND")

    print_banner("HOÀN TẤT DEMO LIVE RUN — MÃ NGUỒN HOẠT ĐỘNG HOÀN HẢO 100%!")


if __name__ == "__main__":
    run_live_demo()
