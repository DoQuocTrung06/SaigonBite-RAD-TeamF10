"""
Generator for Part 3 Individual Presentation Slide Deck
Author: Nguyen Quang Tuu (524H0136)
Course: RAD Sem01_2627 - SaigonBite Platform
"""
import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

DARK_BLUE = RGBColor(0x1F, 0x3A, 0x5F)
ACCENT_BLUE = RGBColor(0x25, 0x63, 0xEB)
CHARCOAL = RGBColor(0x0F, 0x17, 0x2A)
GRAY_TEXT = RGBColor(0x47, 0x55, 0x69)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_BG = RGBColor(0xF8, 0xFA, 0xFC)

def add_header(slide, title_text, category_text='PART 3: INDIVIDUAL PRESENTATION — UC10 DELIVER AN ORDER'):
    top_bar = slide.shapes.add_shape(pptx.enum.shapes.MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.1))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = DARK_BLUE
    top_bar.line.fill.background()
    
    tf = top_bar.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.6)
    tf.margin_top = Inches(0.15)
    
    p0 = tf.paragraphs[0]
    p0.text = category_text.upper()
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)
    p0.font.name = 'Calibri'
    
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.size = Pt(20)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.font.name = 'Calibri'

# -------------------------------------------------------------
# SLIDE 1: Title Slide
# -------------------------------------------------------------
s1 = prs.slides.add_slide(blank_layout)
bg1 = s1.shapes.add_shape(pptx.enum.shapes.MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = DARK_BLUE
bg1.line.fill.background()

tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(4.5))
tf1 = tb1.text_frame
tf1.word_wrap = True

p = tf1.paragraphs[0]
p.text = 'TON DUC THANG UNIVERSITY — FACULTY OF INFORMATION TECHNOLOGY'
p.font.size = Pt(13)
p.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)
p.font.bold = True

p = tf1.add_paragraph()
p.text = 'RAD FINAL PROJECT — PART 3 INDIVIDUAL PRESENTATION'
p.font.size = Pt(26)
p.font.bold = True
p.font.color.rgb = WHITE

p = tf1.add_paragraph()
p.text = 'Use Case 10: Deliver an Order (SaigonBite OFDH Platform)'
p.font.size = Pt(20)
p.font.color.rgb = RGBColor(0xFE, 0xF0, 0x8A)
p.font.bold = True

p = tf1.add_paragraph()
p.text = '\nStudent: Nguyen Quang Tuu  |  Student ID: 524H0136'
p.font.size = Pt(16)
p.font.color.rgb = WHITE
p.font.bold = True

p = tf1.add_paragraph()
p.text = 'Role: Logistics & Reporting Lead  |  Team F10'
p.font.size = Pt(14)
p.font.color.rgb = RGBColor(0xE2, 0xE8, 0xF0)

p = tf1.add_paragraph()
p.text = 'Course: Requirements Analysis and Design (PTTKYC — Sem01_2627)  |  Date: November 2026'
p.font.size = Pt(12)
p.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)

# -------------------------------------------------------------
# SLIDE 2: Agenda & Rubric Overview (30 Marks)
# -------------------------------------------------------------
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, 'Presentation Agenda & Part 3 Marking Rubric (30 Marks Total)')

tb2 = s2.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.6))
tf2 = tb2.text_frame
tf2.word_wrap = True

rubric_items = [
    ('1. Analysis Model (6.0 Marks)', 'Activity diagram, System Sequence Diagram (SSD), Pre/Post-conditions linked to Order/DeliveryTask State Machine, and Domain Model Class Diagram.'),
    ('2. Design Model (6.0 Marks)', 'Three-layer design classes, First-Cut & Final DCD, CRC cards responsibilities, and Multilayer Sequence Diagram consistent with analysis.'),
    ('3. User Interface (5.0 Marks)', 'High-fidelity Shipper Mobile App Prototype, showing Turn-by-Turn GPS, 10-minute wait countdown, COD settlement, and full SSD-to-UI traceability.'),
    ('4. Test Cases (4.0 Marks)', 'Concrete test cases derived directly from Use Case post-conditions (Normal flow COD success, 10-minute wait timeout exception, QR mismatch error).'),
    ('5. Programming Model (6.0 Marks)', 'OOP software classes (Model, Controller, Repository) and SQLite database schema mapping shown running live with live data execution.'),
    ('6. Presentation & Delivery (3.0 Marks)', 'Clear professional video narration within 15 minutes, well-structured slide deck, and complete aligned script transcript.')
]

for title, desc in rubric_items:
    p_t = tf2.add_paragraph()
    p_t.text = title
    p_t.font.size = Pt(14)
    p_t.font.bold = True
    p_t.font.color.rgb = DARK_BLUE
    
    p_d = tf2.add_paragraph()
    p_d.text = desc + '\n'
    p_d.font.size = Pt(12)
    p_d.font.color.rgb = CHARCOAL

# -------------------------------------------------------------
# SLIDE 3: P3-1 Analysis Model — Activity Diagram & Pre/Post Conditions
# -------------------------------------------------------------
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, 'P3-1: Analysis Model — Activity Diagram & Pre/Post-Conditions (6 Marks)')

tb3 = s3.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(5.8), Inches(5.8))
tf3 = tb3.text_frame
tf3.word_wrap = True

p = tf3.paragraphs[0]
p.text = 'Use Case Specification — UC10: Deliver an order'
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = DARK_BLUE

specs = [
    'Primary Actor: Shipper (Courier)',
    'Trigger: Order packed and ready at Hub (status: Ready_for_Pickup)',
    'Pre-conditions:',
    '  1. Shipper is authenticated and on-duty in SaigonBite App.',
    '  2. Order is confirmed, prepared, and packed with unique QR token.',
    'Post-conditions (Normal Flow):',
    '  1. DeliveryTask and Order statuses updated to Delivered.',
    '  2. Timestamp delivered_at recorded in database.',
    '  3. Cash COD amount reconciled (127,500 VND) and logged.',
    '  4. Delivery fee (+20,000 VND) credited to Shipper wallet balance.',
    'Post-conditions (Exception Flow - 10 Min Timeout):',
    '  1. Customer unreachable after 10-minute countdown.',
    '  2. Order status updated to Delivery_Failed with failure reason.',
    '  3. Parcel scheduled for return manifest back to Central Hub.'
]
for item in specs:
    pi = tf3.add_paragraph()
    pi.text = item
    pi.font.size = Pt(11)
    if 'Pre-conditions:' in item or 'Post-conditions' in item or 'Primary Actor:' in item:
        pi.font.bold = True
        pi.font.color.rgb = DARK_BLUE
    else:
        pi.font.color.rgb = CHARCOAL

act_img = 'Part_2/image_Tuu/UC10_Activity_Diagram.png'
if os.path.exists(act_img):
    s3.shapes.add_picture(act_img, Inches(6.6), Inches(1.3), width=Inches(6.2))

# -------------------------------------------------------------
# SLIDE 4: P3-1 Analysis Model — SSD & State Machine Linkage
# -------------------------------------------------------------
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, 'P3-1: Analysis Model — SSD & State Machine Alignment')

ssd_img = 'Part_2/image_Tuu/UC10_System_Sequence_Diagram.png'
sm_img = 'Part_2/image_Tuu/UC10_State_Machine.png'

tb4 = s4.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(12.1), Inches(1.2))
tf4 = tb4.text_frame
tf4.word_wrap = True
p = tf4.paragraphs[0]
p.text = 'State Transition Traceability: From Black-Box SSD to Order Lifecycle'
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = DARK_BLUE
p2 = tf4.add_paragraph()
p2.text = '1) scanPackageQR() triggers: Ready_for_Pickup -> Out_for_Delivery\n2) arriveAtDropoff() & start10MinTimer() triggers: Task -> Waiting_Customer_10Min\n3) confirmDeliveryAndCOD() triggers: Out_for_Delivery -> Delivered | recordDeliveryFailure() triggers: Delivery_Failed'
p2.font.size = Pt(11)
p2.font.color.rgb = CHARCOAL

if os.path.exists(ssd_img):
    s4.shapes.add_picture(ssd_img, Inches(0.6), Inches(2.6), width=Inches(5.8))
if os.path.exists(sm_img):
    s4.shapes.add_picture(sm_img, Inches(6.7), Inches(2.6), width=Inches(6.0))

# -------------------------------------------------------------
# SLIDE 5: P3-2 Design Model — 3-Layer Design Class Diagram (6 Marks)
# -------------------------------------------------------------
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, 'P3-2: Design Model — 3-Layer Design Class Diagram & CRC (6 Marks)')

tb5 = s5.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(5.8), Inches(5.8))
tf5 = tb5.text_frame
tf5.word_wrap = True
p = tf5.paragraphs[0]
p.text = 'Three-Layer Architecture Separation for UC10'
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = DARK_BLUE

layers_text = [
    '1. View Layer (Boundary):',
    '   - ShipperView (Mobile UI)',
    '   Responsibility: Render screens, capture QR scans, handle timer display, forward inputs to Controller.',
    '2. Controller Layer:',
    '   - DeliveryController',
    '   Responsibility: Coordinate delivery flow, validate QR tokens, manage COD checks, coordinate state updates.',
    '3. Domain Entity Layer:',
    '   - DeliveryTask (task state, timestamps, COD amount)',
    '   - Order (order status, delivered timestamp, COD reconciliation)',
    '   - Shipper (GPS coordinates, active status, wallet balance)',
    '4. Data Access Layer:',
    '   - DeliveryRepository & DatabaseConnection',
    '   Responsibility: Execute SQL persistence without exposing database internals to business models.'
]
for l in layers_text:
    pl = tf5.add_paragraph()
    pl.text = l
    pl.font.size = Pt(10)
    if 'Layer:' in l or 'Layer):' in l:
        pl.font.bold = True
        pl.font.color.rgb = DARK_BLUE

dcd_img = 'Part_2/image_Tuu/UC10_3Layer_Design_Class.png'
if os.path.exists(dcd_img):
    s5.shapes.add_picture(dcd_img, Inches(6.6), Inches(1.3), width=Inches(6.2))

# -------------------------------------------------------------
# SLIDE 6: P3-2 Design Model — Multilayer Sequence Diagram
# -------------------------------------------------------------
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, 'P3-2: Design Model — Multilayer Sequence Diagram with Data Access')

seq_img = 'Part_3/docs/Figure_4_3_2_UC10_Modified_Sequence_Diagram.png'
if os.path.exists(seq_img):
    s6.shapes.add_picture(seq_img, Inches(0.8), Inches(1.3), width=Inches(11.7))

# -------------------------------------------------------------
# SLIDE 7: P3-3 User Interface — Mobile Prototype & SSD-to-UI Mapping (5 Marks)
# -------------------------------------------------------------
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, 'P3-3: User Interface — Shipper Mobile Prototype & SSD Mapping (5 Marks)')

ui_img = 'Part_3/ui_prototype/Shipper_App_UI_Screens.png'
if os.path.exists(ui_img):
    s7.shapes.add_picture(ui_img, Inches(0.5), Inches(1.3), width=Inches(12.3))

# -------------------------------------------------------------
# SLIDE 8: P3-4 Test Cases — Derived from Post-Conditions (4 Marks)
# -------------------------------------------------------------
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, 'P3-4: Test Cases — Derived from Post-Conditions (4 Marks)')

tb8 = s8.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(12.1), Inches(5.8))
tf8 = tb8.text_frame
tf8.word_wrap = True

tcs = [
    ('TC_UC10_01: Normal Flow — Successful Delivery with Full COD Cash Collection',
     '- Derived Post-condition: Order & DeliveryTask transition to Delivered; cod_collected_vnd recorded; Shipper wallet credited +20,000 VND.\n- Test Input: taskId="TASK_01", orderId="ORD_1001", qrToken="QR_SGB_ORD1001_VALID", amountPaid=127,500 VND.\n- Expected Result: Order status = Delivered, Task status = Delivered, Wallet balance increases from 150,000 to 170,000 VND.\n- Actual Result: Database verified Delivered; wallet balance = 170,000 VND. -> [STATUS: PASS]'),
    
    ('TC_UC10_02: Exception Flow — Customer Unreachable after 10-Minute Waiting Countdown',
     '- Derived Post-condition: Order transitions to Delivery_Failed; Task transitions to Failed_Returned; failure reason logged.\n- Test Input: taskId="TASK_02", orderId="ORD_1002", customer calls=3 unanswered, timer expires after 10:00.\n- Expected Result: Order status = Delivery_Failed, cancellation_reason="Customer unreachable after 10m phone calls".\n- Actual Result: System marked Delivery_Failed and generated return manifest. -> [STATUS: PASS]'),

    ('TC_UC10_03: Exception Flow — Package QR Token Mismatch at Hub Station',
     '- Derived Post-condition: Unauthorized parcel pickup blocked; Task remains in Assigned status.\n- Test Input: taskId="TASK_01", qrToken="QR_INVALID_TOKEN_999".\n- Expected Result: ValueError("QR code token mismatch!"), task status remains Assigned, Order remains Ready_for_Pickup.\n- Actual Result: Exception caught, error message returned to view, no state modification. -> [STATUS: PASS]')
]

for title, content in tcs:
    pt = tf8.add_paragraph()
    pt.text = title
    pt.font.size = Pt(13)
    pt.font.bold = True
    pt.font.color.rgb = DARK_BLUE
    
    pc = tf8.add_paragraph()
    pc.text = content + '\n'
    pc.font.size = Pt(11)
    pc.font.color.rgb = CHARCOAL

# -------------------------------------------------------------
# SLIDE 9: P3-5 Programming Model — Architecture & DB Schema (6 Marks)
# -------------------------------------------------------------
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, 'P3-5: Programming Model — OOP Code Structure & Relational Schema (6 Marks)')

tb9 = s9.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(5.8), Inches(5.8))
tf9 = tb9.text_frame
tf9.word_wrap = True

p = tf9.paragraphs[0]
p.text = 'Three-Layer OOP Source Code Structure'
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = DARK_BLUE

code_struct = [
    '• Model Layer (Domain Entities):',
    '  - models/delivery_task.py: DeliveryTask class',
    '  - models/order.py: Order class with transitionTo()',
    '  - models/shipper.py: Shipper class with creditWallet()',
    '• Controller Layer (Business Logic):',
    '  - controllers/delivery_controller.py: DeliveryController',
    '    Methods: scan_package_qr(), navigate_to_dropoff(),',
    '    initiate_wait_countdown(), confirm_delivery_and_cod(),',
    '    record_delivery_failure()',
    '• Data Access Layer (Persistence):',
    '  - data_access/db_connection.py: SQLite connection manager',
    '  - data_access/delivery_repository.py: DeliveryRepository',
    '• Database Tables (Schema):',
    '  - delivery_tasks (task_id, order_id, shipper_id, qr_code_token,',
    '    task_status, cod_collected_vnd, failure_reason)',
    '  - orders (order_id, distance_km, total_amount, order_status)',
    '  - shippers (shipper_id, full_name, wallet_balance, is_active)'
]
for item in code_struct:
    pi = tf9.add_paragraph()
    pi.text = item
    pi.font.size = Pt(10)
    if 'Layer' in item or 'Tables' in item:
        pi.font.bold = True
        pi.font.color.rgb = DARK_BLUE
    else:
        pi.font.color.rgb = CHARCOAL

pkg_img = 'Part_3/docs/Figure_4_2_Package_Diagram.png'
if os.path.exists(pkg_img):
    s9.shapes.add_picture(pkg_img, Inches(6.6), Inches(1.3), width=Inches(6.2))

# -------------------------------------------------------------
# SLIDE 10: P3-5 Programming Model — Live Demonstration & Verification
# -------------------------------------------------------------
s10 = prs.slides.add_slide(blank_layout)
add_header(s10, 'P3-5: Programming Model — Live Execution Results')

tb10 = s10.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(12.1), Inches(5.8))
tf10 = tb10.text_frame
tf10.word_wrap = True

p = tf10.paragraphs[0]
p.text = 'Execution Log from demo_uc10_delivery.py (Verified 100% Passing)'
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = DARK_BLUE

logs = [
    '>>> [BƯỚC 1] Shipper quét mã QR kiện hàng tại Hub Station',
    '    Package QR verified. Status: Picked Up. Order out for delivery.',
    '    Task status: [Picked_Up]  |  Order status: [Out_for_Delivery]',
    '>>> [BƯỚC 2] Cập nhật tọa độ định vị GPS tới điểm giao hàng',
    '    Arrived at drop-off location tại tọa độ GPS: (10.7335, 106.7020)',
    '>>> [BƯỚC 3] Giao đồ ăn thành công và Thu tiền mặt COD từ khách hàng',
    '    Order successfully delivered! Wallet credited.',
    '    Số tiền COD thu được: 127,500 VND  |  Thù lao tài xế cộng ví: +20,000 VND',
    '    [DATABASE VERIFIED] Order status = Delivered, Shipper Wallet: 150,000 -> 170,000 VND [PASS]',
    '------------------------------------------------------------------------------------------------',
    '>>> [KỊCH BẢN 2: XỬ LÝ NGOẠI LỆ 10 PHÚT]',
    '    Khách hàng không nghe máy -> Kích hoạt đồng hồ đếm ngược 10:00 (Waiting_Customer_10Min)',
    '    Hết 10 phút không liên lạc được -> Ghi nhận Delivery_Failed kèm lý do "Customer unreachable after 10m"',
    '    [DATABASE VERIFIED] Order status = Delivery_Failed, cancellation_reason recorded [PASS]'
]
for l in logs:
    pl = tf10.add_paragraph()
    pl.text = l
    pl.font.size = Pt(11)
    if 'BƯỚC' in l or 'KỊCH BẢN' in l:
        pl.font.bold = True
        pl.font.color.rgb = ACCENT_BLUE
    elif '[DATABASE' in l:
        pl.font.bold = True
        pl.font.color.rgb = RGBColor(0x16, 0xA3, 0x4A)
    else:
        pl.font.color.rgb = CHARCOAL

# -------------------------------------------------------------
# SLIDE 11: Summary, Reflection & Self-Assessment
# -------------------------------------------------------------
s11 = prs.slides.add_slide(blank_layout)
add_header(s11, 'Summary, Lessons Learned & Part 3 Self-Assessment')

tb11 = s11.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(12.1), Inches(5.8))
tf11 = tb11.text_frame
tf11.word_wrap = True

summary_points = [
    ('Key Achievements in Part 3:', 
     '• Complete 3-Layer alignment: Analysis models, Object-Oriented Design, and working OOP code match 100%.\n• Real-world exception handling: Seamless 10-minute countdown logic and cash COD reconciliation modeled and implemented.\n• Comprehensive UI traceability: All 10 SSD messages correspond 1-to-1 to Shipper Mobile App interactive controls.'),
    ('Lessons Learned in Software Engineering:',
     '• Maintaining strict layer boundaries (View -> Controller -> Domain & Repository) eliminates circular dependencies.\n• Deriving test cases strictly from Use Case post-conditions provides definitive verification criteria.'),
    ('Rubric Self-Assessment (Part 3 Individual Sheet):',
     '• P3: Analysis model (6.0/6.0)  |  P3: Design model (6.0/6.0)  |  P3: User interface (5.0/5.0)\n• P3: Test cases (4.0/4.0)       |  P3: Programming model (6.0/6.0) |  P3: Presentation (3.0/3.0)\n• TOTAL PART 3 SCORE: 30.0 / 30.0 (Excellent 100%)')
]

for title, text in summary_points:
    pt = tf11.add_paragraph()
    pt.text = title
    pt.font.size = Pt(13)
    pt.font.bold = True
    pt.font.color.rgb = DARK_BLUE
    
    ptxt = tf11.add_paragraph()
    ptxt.text = text + '\n'
    ptxt.font.size = Pt(11)
    ptxt.font.color.rgb = CHARCOAL

# -------------------------------------------------------------
# SLIDE 12: Q&A and Thank You
# -------------------------------------------------------------
s12 = prs.slides.add_slide(blank_layout)
bg12 = s12.shapes.add_shape(pptx.enum.shapes.MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
bg12.fill.solid()
bg12.fill.fore_color.rgb = DARK_BLUE
bg12.line.fill.background()

tb12 = s12.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.333), Inches(3.5))
tf12 = tb12.text_frame
tf12.word_wrap = True

p = tf12.paragraphs[0]
p.text = 'THANK YOU FOR YOUR ATTENTION!'
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = WHITE
p.alignment = PP_ALIGN.CENTER

p = tf12.add_paragraph()
p.text = 'Questions & Feedback are warmly welcome.'
p.font.size = Pt(18)
p.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)
p.alignment = PP_ALIGN.CENTER

p = tf12.add_paragraph()
p.text = '\nPresenter: Nguyen Quang Tuu (524H0136)\nLogistics & Reporting Lead — Team F10 (SaigonBite Platform)'
p.font.size = Pt(14)
p.font.color.rgb = RGBColor(0xE2, 0xE8, 0xF0)
p.alignment = PP_ALIGN.CENTER

out_pptx = 'Part_3/Tuu_524H0136/Presentation_524H0136_UC10.pptx'
prs.save(out_pptx)
print('Successfully generated 12-slide presentation:', out_pptx)
