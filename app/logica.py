import os
import sys
from datetime import datetime

# Imports robustos para funcionar como paquete o script
try:
    # Ejecutando como paquete: python -m app.main
    from app.database import registrar_pedido, obtener_balance, obtener_historial
    from app.tickets import generar_ticket_pdf, generar_ticket_txt
except Exception:
    # Ejecutando directo (no recomendado)
    BASE_DIR = os.path.dirname(__file__)
    if BASE_DIR not in sys.path:
        sys.path.append(BASE_DIR)
    from database import registrar_pedido, obtener_balance, obtener_historial
    from tickets import generar_ticket_pdf, generar_ticket_txt

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
TICKETS_DIR = os.path.join(DATA_DIR, "tickets")
os.makedirs(TICKETS_DIR, exist_ok=True)

# ----------------- Pedido en memoria -----------------
def agregar_producto(pedido, producto, cantidad, precio):
    """Agrega un producto al pedido (lista de dicts)."""
    if not producto or cantidad <= 0 or precio < 0:
        return False, "Datos inválidos."
    pedido.append({
        "producto": producto.strip(),
        "cantidad": int(cantidad),
        "precio": float(precio)
    })
    return True, "Producto agregado."

def editar_producto(pedido, indice, nueva_cantidad):
    """Edita la cantidad de un producto existente por índice."""
    if indice < 0 or indice >= len(pedido):
        return False, "Índice inválido."
    if nueva_cantidad <= 0:
        return False, "La cantidad debe ser mayor a 0."
    pedido[indice]["cantidad"] = int(nueva_cantidad)
    return True, "Cantidad actualizada."

def eliminar_producto(pedido, indice):
    """Elimina un item del pedido por índice."""
    if indice < 0 or indice >= len(pedido):
        return False, "Índice inválido."
    pedido.pop(indice)
    return True, "Producto eliminado."

def calcular_total(pedido):
    """Suma total del pedido."""
    return float(sum(it["cantidad"] * it["precio"] for it in pedido))

# ----------------- Procesamiento (BD + Ticket) -----------------
def procesar_pedido(pedido, generar_pdf=True):
    """
    Registra en BD y genera ticket (PDF si es posible; si no, TXT).
    Devuelve dict con ok, total, ticket, formato, mensaje.
    """
    if not pedido:
        return {"ok": False, "mensaje": "El pedido está vacío."}

    total = registrar_pedido(pedido)

    # Intentar PDF
    ruta = None
    formato = None
    if generar_pdf:
        ok_pdf, res_pdf = generar_ticket_pdf(pedido)
        if ok_pdf:
            ruta, formato = res_pdf, "PDF"
        else:
            # Fallback TXT
            ok_txt, res_txt = generar_ticket_txt(pedido)
            if ok_txt:
                ruta, formato = res_txt, "TXT"
            else:
                return {"ok": True, "total": total, "ticket": None, "formato": None,
                        "mensaje": f"Venta registrada. Problema al generar ticket: {res_pdf} / {res_txt}"}
    else:
        ok_txt, res_txt = generar_ticket_txt(pedido)
        ruta, formato = (res_txt, "TXT") if ok_txt else (None, None)

    return {"ok": True, "total": total, "ticket": ruta, "formato": formato,
            "mensaje": "Pedido procesado."}

def listar_tickets(limit=30):
    """Lista tickets ordenados por fecha descendente."""
    if not os.path.isdir(TICKETS_DIR):
        return []
    files = [os.path.join(TICKETS_DIR, f) for f in os.listdir(TICKETS_DIR)]
    files = [f for f in files if os.path.isfile(f)]
    files.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return files[:limit]

# ----------------- IA simple (placeholder) -----------------
def sugerir_producto(historial=None):
    """
    Devuelve una sugerencia simple (placeholder IA).
    Si no hay historial, sugiere un combo popular.
    """
    # Podrías usar 'obtener_historial()' para calcular top ventas.
    return "Combo Pollo a la Brasa + Inka Kola"
