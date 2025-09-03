import os
from datetime import datetime
from reportlab.lib.pagesizes import A6
from reportlab.pdfgen import canvas

# Carpeta para guardar los tickets
TICKETS_DIR = os.path.join("data", "tickets")
os.makedirs(TICKETS_DIR, exist_ok=True)

def generar_ticket_pdf(pedido):
    """Genera un ticket PDF del pedido"""
    if not pedido:
        return False, "El pedido está vacío."

    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo_pdf = os.path.join(TICKETS_DIR, f"ticket_{fecha}.pdf")

    total = sum(p["cantidad"] * p["precio"] for p in pedido)

    c = canvas.Canvas(archivo_pdf, pagesize=A6)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, 380, "=== Restaurante POS ===")
    c.setFont("Helvetica", 10)
    c.drawString(10, 360, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    c.drawString(10, 345, "-" * 28)

    y = 330
    for item in pedido:
        subtotal = item["cantidad"] * item["precio"]
        c.drawString(10, y, f"{item['producto']} x{item['cantidad']} - S/ {subtotal:.2f}")
        y -= 15

    c.drawString(10, y - 5, "-" * 28)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(10, y - 20, f"TOTAL: S/ {total:.2f}")
    c.setFont("Helvetica", 9)
    c.drawString(10, y - 40, "¡Gracias por su compra!")
    c.save()

    return True, archivo_pdf
