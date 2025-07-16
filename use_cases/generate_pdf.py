from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from core.invoice import Invoice

def generate_pdf(invoice: Invoice, file_path: str):
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1 * inch, height - 1 * inch, "Factura")

    # Información del cliente y fecha
    c.setFont("Helvetica", 12)
    c.drawString(1 * inch, height - 1.5 * inch, f"Cliente: {invoice.client}")
    c.drawString(1 * inch, height - 1.7 * inch, f"Fecha: {invoice.date.strftime('%Y-%m-%d')}")

    # Cabeceras de la tabla de ítems
    c.setFont("Helvetica-Bold", 12)
    y_position = height - 2.5 * inch
    c.drawString(1 * inch, y_position, "Descripción")
    c.drawString(4 * inch, y_position, "Cantidad")
    c.drawString(5 * inch, y_position, "Precio Unitario")
    c.drawString(6.5 * inch, y_position, "Total")

    # Ítems de la factura
    c.setFont("Helvetica", 12)
    y_position -= 0.25 * inch
    for item in invoice.items:
        c.drawString(1 * inch, y_position, item.description)
        c.drawString(4 * inch, y_position, str(item.quantity))
        c.drawString(5 * inch, y_position, f"${item.price:.2f}")
        c.drawString(6.5 * inch, y_position, f"${item.total():.2f}")
        y_position -= 0.25 * inch

    # Total de la factura
    c.setFont("Helvetica-Bold", 14)
    y_position -= 0.5 * inch
    c.drawString(5 * inch, y_position, "Total:")
    c.drawString(6.5 * inch, y_position, f"${invoice.total():.2f}")

    c.save()
