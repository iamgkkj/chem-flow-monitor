from __future__ import annotations

from io import BytesIO

from reportlab.graphics import renderPDF
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.legends import Legend
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
        c.showPage()

        d_w = width - 4 * cm
        d_h = 12 * cm
        drawing = Drawing(d_w, d_h)

        pie = Pie()
        pie.x = 0.5 * cm
        pie.y = 0.8 * cm
        pie.width = (d_w / 2) - 1.0 * cm
        pie.height = d_h - 1.6 * cm
        pie.data = values
        pie.labels = [
            f"{name} ({(val / total * 100):.0f}%)" if total else f"{name}"
            for name, val in zip(labels, values)
        ]
        pie.slices.strokeWidth = 0.5
        pie.slices.strokeColor = colors.white
        palette = [
            colors.HexColor('#1d4ed8'),
            colors.HexColor('#2563eb'),
            colors.HexColor('#3b82f6'),
            colors.HexColor('#60a5fa'),
            colors.HexColor('#93c5fd'),
            colors.HexColor('#0ea5e9'),
            colors.HexColor('#0284c7'),
            colors.HexColor('#075985'),
        ]
        for i in range(len(values)):
            pie.slices[i].fillColor = palette[i % len(palette)]
        pie.sideLabels = True
        pie.simpleLabels = False

        bar = VerticalBarChart()
        bar.x = (d_w / 2) + 0.5 * cm
        bar.y = 0.8 * cm
        bar.width = (d_w / 2) - 1.0 * cm
        bar.height = d_h - 2.2 * cm
        bar.data = [values]
        bar.categoryAxis.categoryNames = labels
        bar.categoryAxis.labels.boxAnchor = 'ne'
        bar.categoryAxis.labels.angle = 45
        bar.categoryAxis.labels.dx = -6
        bar.categoryAxis.labels.dy = -2
        bar.valueAxis.valueMin = 0
        bar.bars[0].fillColor = colors.HexColor('#2563eb')
        bar.barSpacing = 2

        legend = Legend()
        legend.x = 0.5 * cm
        legend.y = d_h - 0.2 * cm
        legend.alignment = 'left'
        legend.fontName = 'Helvetica'
        legend.fontSize = 9
        legend.dx = 6
        legend.dy = 6
        legend.columnMaximum = 1
        legend.colorNamePairs = [
            (colors.HexColor('#2563eb'), 'Pie: Type share (with % labels)  |  Bar: Type counts'),
        ]

        drawing.add(pie)
        drawing.add(bar)
        drawing.add(legend)

        c.setFont('Helvetica-Bold', 14)
        c.drawString(2 * cm, height - 2 * cm, 'Equipment Type Charts')
        renderPDF.draw(drawing, c, 2 * cm, height - 2 * cm - d_h - 0.8 * cm)

    c.save()
    buffer.seek(0)
    return buffer.read()
