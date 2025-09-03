import os
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
TICKETS_DIR = os.path.join(DATA_DIR, "tickets")
os.makedirs(TICKETS_DIR, exist_ok=True)

def generar_ticket_pdf(pedido):
    """
    Intenta generar PDF con reportlab. Si no está instalado,
    devuelve (False, mensaje).
    """
    try:
        from reportlab.lib.pagesizes import A6
        from reportlab.pdfgen import canvas
    except Exception:
        return False, "Falta 'reportlab'. Instala con: python -m pip install reportlab"

    if not pedido:
        return False, "El pedido está vacío."

    fecha_slug = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo_pdf = os.path.join(TICKETS_DIR, f"ticket_{fecha_slug}.pdf")
    total = sum(p["cantidad"] * p["precio"] for p in pedido)

    c = canvas.Canvas(archivo_pdf, pagesize=A6)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20, 380, "=== Restaurante POS ===")
    c.setFont("Helvetica", 9)
    c.drawString(20, 365, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    c.drawString(20, 353, "-" * 28)

    y = 338
    for item in pedido:
        subtotal = item["cantidad"] * item["precio"]
        linea = f"{item['producto']} x{item['cantidad']}  S/ {subtotal:.2f}"
        c.drawString(20, y, linea)
        y -= 12

    c.drawString(20, y - 3, "-" * 28)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(20, y - 18, f"TOTAL: S/ {total:.2f}")
    c.setFont("Helvetica", 9)
    c.drawString(20, y - 36, "¡Gracias por su compra!")
    c.save()

    return True, archivo_pdf

def generar_ticket_txt(pedido):
    """Genera un ticket TXT como respaldo."""
    if not pedido:
        return False, "El pedido está vacío."
    fecha_slug = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo = os.path.join(TICKETS_DIR, f"ticket_{fecha_slug}.txt")
    total = sum(it["cantidad"] * it["precio"] for it in pedido)
    with open(archivo, "w", encoding="utf-8") as f:
        f.write("===== TICKET RESTAURANTE POS =====\n")
        f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("-----------------------------------\n")
        for it in pedido:
            f.write(f"{it['producto']} x{it['cantidad']}  S/ {it['cantidad']*it['precio']:.2f}\n")
        f.write("-----------------------------------\n")
        f.write(f"TOTAL: S/ {total:.2f}\n")
        f.write("¡Gracias por su compra!\n")
    return True, archivo
