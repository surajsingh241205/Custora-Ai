import os
import base64
import io
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4


def generate_pdf_report(
    file_path,
    total,
    high,
    medium,
    low,
    ai_summary,
    chart_image_base64=None
):

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # ================= HEADER =================

    logo_path = os.path.join("static", "images", "2.png")

    if os.path.exists(logo_path):
        elements.append(Image(logo_path, width=3.15 * inch, height=0.6 * inch))

    elements.append(Spacer(1, 0.2 * inch))

    elements.append(
        Paragraph(
            "<b>Custora AI - Customer Risk Intelligence Report</b>",
            styles["Heading1"]
        )
    )

    elements.append(
        Paragraph(
            f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 0.3 * inch))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    elements.append(Spacer(1, 0.3 * inch))

    # ================= EXECUTIVE SUMMARY =================

    if isinstance(ai_summary, dict) and ai_summary.get("summary"):
        elements.append(Paragraph("<b>Executive Summary</b>", styles["Heading2"]))
        elements.append(Spacer(1, 0.15 * inch))
        elements.append(
            Paragraph(ai_summary.get("summary", ""), styles["Normal"])
        )
        elements.append(Spacer(1, 0.3 * inch))

    # ================= RISK TABLE =================

    elements.append(Paragraph("<b>Risk Overview</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.15 * inch))

    data = [
        ["Metric", "Value"],
        ["Total Customers", str(total)],
        ["High Risk", str(high)],
        ["Medium Risk", str(medium)],
        ["Low Risk", str(low)]
    ]

    table = Table(data, colWidths=[3 * inch, 2 * inch])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.4 * inch))

    # ================= CHART IMAGE =================

    if chart_image_base64 and "," in chart_image_base64:
        try:
            elements.append(
                Paragraph("<b>Risk Distribution Chart</b>", styles["Heading2"])
            )
            elements.append(Spacer(1, 0.2 * inch))

            chart_data = base64.b64decode(chart_image_base64.split(",")[1])
            image_stream = io.BytesIO(chart_data)

            elements.append(
                Image(image_stream, width=5.5 * inch, height=3 * inch)
            )

        except Exception as e:
            print("Chart embedding failed:", e)

    doc.build(elements)
