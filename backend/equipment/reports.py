from __future__ import annotations

from io import BytesIO

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

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()
