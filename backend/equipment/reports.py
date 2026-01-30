from __future__ import annotations

from io import BytesIO

from reportlab.graphics import renderPDF
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from .models import Dataset


def build_dataset_report_pdf(dataset: Dataset) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 2 * cm
    c.setFont('Helvetica-Bold', 16)
    c.drawString(2 * cm, y, 'Equipment Dataset Report')

    y -= 1.2 * cm
    c.setFont('Helvetica', 11)
    c.drawString(2 * cm, y, f'Dataset ID: {dataset.id}')

    y -= 0.6 * cm
    c.drawString(2 * cm, y, f'Uploaded: {dataset.created_at.isoformat()}')

    y -= 0.6 * cm
    c.drawString(2 * cm, y, f'Filename: {dataset.original_filename}')

    y -= 1.0 * cm
    c.setFont('Helvetica-Bold', 12)
    c.drawString(2 * cm, y, 'Summary')

    y -= 0.8 * cm
    c.setFont('Helvetica', 11)
    c.drawString(2 * cm, y, f'Total equipment count: {dataset.total_count}')

    y -= 0.6 * cm
    c.drawString(2 * cm, y, f'Average Flowrate: {dataset.avg_flowrate}')

    y -= 0.6 * cm
    c.drawString(2 * cm, y, f'Average Pressure: {dataset.avg_pressure}')

    y -= 0.6 * cm
    c.drawString(2 * cm, y, f'Average Temperature: {dataset.avg_temperature}')

    y -= 1.0 * cm
    c.setFont('Helvetica-Bold', 12)
    c.drawString(2 * cm, y, 'Equipment Type Distribution')

    y -= 0.8 * cm
    c.setFont('Helvetica', 11)

    for k, v in (dataset.type_distribution or {}).items():
        if y < 2 * cm:
            c.showPage()
            y = height - 2 * cm
            c.setFont('Helvetica', 11)

        c.drawString(2 * cm, y, f'{k}: {v}')
        y -= 0.5 * cm

    dist = dataset.type_distribution or {}
    labels = list(dist.keys())
    values = [float(dist[k]) for k in labels]
    total = sum(values) if values else 0.0

    if labels and values:
        palette = [
            colors.HexColor('#4e79a7'),
            colors.HexColor('#f28e2b'),
            colors.HexColor('#e15759'),
            colors.HexColor('#76b7b2'),
            colors.HexColor('#59a14f'),
            colors.HexColor('#edc949'),
            colors.HexColor('#af7aa1'),
            colors.HexColor('#ff9da7'),
            colors.HexColor('#9c755f'),
            colors.HexColor('#bab0ab'),
        ]

        d_w = width - 4 * cm
        d_h = height - 6 * cm
        draw_x = (width - d_w) / 2
        draw_y = 2 * cm

        c.showPage()
        c.setFont('Helvetica-Bold', 14)
        c.drawCentredString(width / 2, height - 2 * cm, 'Equipment Type Distribution (Pie Chart)')

        pie_drawing = Drawing(d_w, d_h)
        pie = Pie()

        pie_size = min(d_w, d_h) - 2.0 * cm
        pie.x = (d_w - pie_size) / 2
        pie.y = (d_h - pie_size) / 2
        pie.width = pie_size
        pie.height = pie_size
        pie.data = values
        pie.labels = [
            f"{name} ({(val / total * 100):.0f}%)" if total else f"{name}"
            for name, val in zip(labels, values)
        ]
        pie.slices.strokeWidth = 0.5
        pie.slices.strokeColor = colors.white
        for i in range(len(values)):
            pie.slices[i].fillColor = palette[i % len(palette)]
        pie.sideLabels = True
        pie.simpleLabels = False

        pie_drawing.add(pie)
        renderPDF.draw(pie_drawing, c, draw_x, draw_y)

        c.showPage()
        c.setFont('Helvetica-Bold', 14)
        c.drawCentredString(width / 2, height - 2 * cm, 'Equipment Type Counts (Bar Chart)')

        bar_drawing = Drawing(d_w, d_h)
        bar = VerticalBarChart()
        bar.x = 1.0 * cm
        bar.y = 1.0 * cm
        bar.width = d_w - 2.0 * cm
        bar.height = d_h - 2.5 * cm
        bar.data = [values]
        bar.categoryAxis.categoryNames = labels
        bar.categoryAxis.labels.boxAnchor = 'ne'
        bar.categoryAxis.labels.angle = 45
        bar.categoryAxis.labels.dx = -6
        bar.categoryAxis.labels.dy = -2
        bar.valueAxis.valueMin = 0
        bar.bars[0].fillColor = colors.HexColor('#2563eb')
        bar.barSpacing = 2

        bar_drawing.add(bar)
        renderPDF.draw(bar_drawing, c, draw_x, draw_y)

    c.save()
    buffer.seek(0)
    return buffer.read()
