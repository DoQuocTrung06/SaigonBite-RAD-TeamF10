"""
Convert Transcript Markdown to Word Docx
Author: Nguyen Quang Tuu (524H0136)
Course: RAD Sem01_2627 - SaigonBite Platform
"""
import os
import docx
from docx.shared import Inches, Pt, RGBColor

doc = docx.Document()

# Set standard margins
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Title
title_p = doc.add_paragraph()
title_run = title_p.add_run("KỊCH BẢN THUYẾT TRÌNH VIDEO CÁ NHÂN (PART 3 TRANSCRIPT)\n")
title_run.font.name = "Calibri"
title_run.font.size = Pt(18)
title_run.font.bold = True
title_run.font.color.rgb = RGBColor(0x1F, 0x3A, 0x5F)

sub_p = doc.add_paragraph()
sub_run = sub_p.add_run(
    "Học phần: Phân tích và Thiết kế Yêu cầu (RAD Sem01_2627) — Đại học Tôn Đức Thắng\n"
    "Sinh viên: Nguyễn Quang Tựu | MSSV: 524H0136 | Nhóm: Team F10 (SaigonBite)\n"
    "Use Case: UC10 — Deliver an order (Giao hàng, định vị GPS, đợi 10 phút, thu COD)\n"
    "Thời lượng: 10 - 12 phút (Khớp hoàn toàn với slide Presentation_524H0136_UC10.pptx)\n"
    "----------------------------------------------------------------------------------------"
)
sub_run.font.name = "Calibri"
sub_run.font.size = Pt(11)
sub_run.font.italic = True
sub_run.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

md_path = os.path.join(os.path.dirname(__file__), "Transcript_524H0136_UC10.md")
with open(md_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    line_s = line.strip()
    if not line_s or line_s.startswith("# ") or line_s.startswith("---"):
        continue
    
    p = doc.add_paragraph()
    if line_s.startswith("## "):
        r = p.add_run(line_s.replace("## ", ""))
        r.font.name = "Calibri"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x1F, 0x3A, 0x5F)
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
    elif line_s.startswith("> "):
        clean_text = line_s.replace("> ", "").replace('"', "")
        r = p.add_run(clean_text)
        r.font.name = "Calibri"
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(6)
    else:
        r = p.add_run(line_s)
        r.font.name = "Calibri"
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        p.paragraph_format.space_after = Pt(4)

out_doc = os.path.join(os.path.dirname(__file__), "Transcript_524H0136_UC10.docx")
doc.save(out_doc)
print(f"Saved Word Transcript to: {out_doc}")
