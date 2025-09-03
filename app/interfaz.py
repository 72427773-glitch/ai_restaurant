import tkinter as tk
from tkinter import ttk, messagebox

# Imports robustos
try:
    from app.logica import (
        agregar_producto, editar_producto, eliminar_producto,
        calcular_total, procesar_pedido, listar_tickets, sugerir_producto
    )
except Exception:
    from logica import (
        agregar_producto, editar_producto, eliminar_producto,
        calcular_total, procesar_pedido, listar_tickets, sugerir_producto
    )

PRODUCTOS_BASE = [
    ("Pollo a la Brasa 1/4", 18.0),
    ("Ceviche Clásico", 24.0),
    ("Lomo Saltado", 22.0),
    ("Chaufa Mixto", 20.0),
    ("Inka Kola 500ml", 5.0),
    ("Chicha Morada 500ml", 5.0),
]

def iniciar_app():
    root = tk.Tk()
    root.title("Restaurante POS")
    root.geometry("820x560")

    pedido = []

    # ---- Frame Menú ----
    frm_menu = ttk.LabelFrame(root, text="Menú")
    frm_menu.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)

    lbl_prod = ttk.Label(frm_menu, text="Producto")
    lbl_prod.pack(anchor="w", padx=6, pady=(6, 0))
    cmb_prod = ttk.Combobox(frm_menu, values=[p[0] for p in PRODUCTOS_BASE], state="readonly", width=28)
    cmb_prod.pack(padx=6, pady=4)
    cmb_prod.current(0)

    lbl_precio = ttk.Label(frm_menu, text="Precio (S/)")
    lbl_precio.pack(anchor="w", padx=6)
    var_precio = tk.StringVar(value=str(PRODUCTOS_BASE[0][1]))
    ent_precio = ttk.Entry(frm_menu, textvariable=var_precio, width=10)
    ent_precio.pack(padx=6, pady=4)

    def on_select(event=None):
        i = cmb_prod.current()
        if i >= 0:
            var_precio.set(str(PRODUCTOS_BASE[i][1]))
    cmb_prod.bind("<<ComboboxSelected>>", on_select)

    lbl_cant = ttk.Label(frm_menu, text="Cantidad")
    lbl_cant.pack(anchor="w", padx=6)
    var_cant = tk.IntVar(value=1)
    spn_cant = ttk.Spinbox(frm_menu, from_=1, to=50, textvariable=var_cant, width=8)
    spn_cant.pack(padx=6, pady=4)

    def ui_agregar():
        prod = cmb_prod.get()
        try:
            precio = float(var_precio.get())
        except ValueError:
            messagebox.showerror("Error", "Precio inválido.")
            return
        cant = var_cant.get()
        ok, msg = agregar_producto(pedido, prod, cant, precio)
        if not ok:
            messagebox.showerror("Error", msg)
        refrescar_pedido()

    btn_add = ttk.Button(frm_menu, text="Agregar", command=ui_agregar)
    btn_add.pack(padx=6, pady=6, fill="x")

    lbl_sug = ttk.Label(frm_menu, text="Sugerencia IA:")
    lbl_sug.pack(anchor="w", padx=6, pady=(12, 0))
    var_sug = tk.StringVar(value=sugerir_producto())
    ent_sug = ttk.Entry(frm_menu, textvariable=var_sug, state="readonly")
    ent_sug.pack(padx=6, pady=(0, 6), fill="x")

    # ---- Frame Pedido ----
    frm_pedido = ttk.LabelFrame(root, text="Pedido")
    frm_pedido.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

    cols = ("Producto", "Cant.", "Precio", "Subtotal")
    tree = ttk.Treeview(frm_pedido, columns=cols, show="headings", height=12)
    for c in cols:
        tree.heading(c, text=c)
    tree.column("Producto", width=200)
    tree.column("Cant.", width=60, anchor="center")
    tree.column("Precio", width=80, anchor="e")
    tree.column("Subtotal", width=90, anchor="e")
    tree.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    frm_acciones = ttk.Frame(frm_pedido)
    frm_acciones.pack(fill="x", padx=6, pady=4)

    lbl_edit = ttk.Label(frm_acciones, text="Nueva cantidad:")
    lbl_edit.pack(side="left")
    var_edit = tk.IntVar(value=1)
    spn_edit = ttk.Spinbox(frm_acciones, from_=1, to=50, textvariable=var_edit, width=6)
    spn_edit.pack(side="left", padx=4)

    def ui_editar():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un item.")
            return
        idx = tree.index(sel[0])
        ok, msg = editar_producto(pedido, idx, var_edit.get())
        if not ok:
            messagebox.showerror("Error", msg)
        refrescar_pedido()

    def ui_eliminar():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un item.")
            return
        idx = tree.index(sel[0])
        ok, msg = eliminar_producto(pedido, idx)
        if not ok:
            messagebox.showerror("Error", msg)
        refrescar_pedido()

    ttk.Button(frm_acciones, text="Editar", command=ui_editar).pack(side="left", padx=4)
    ttk.Button(frm_acciones, text="Eliminar", command=ui_eliminar).pack(side="left", padx=4)

    frm_total = ttk.Frame(frm_pedido)
    frm_total.pack(fill="x", padx=6, pady=6)
    ttk.Label(frm_total, text="TOTAL (S/):", font=("Segoe UI", 12, "bold")).pack(side="left")
    var_total = tk.StringVar(value="0.00")
    ttk.Label(frm_total, textvariable=var_total, font=("Segoe UI", 12, "bold")).pack(side="left", padx=6)

    def refrescar_pedido():
        for i in tree.get_children():
            tree.delete(i)
        for it in pedido:
            subtotal = it["cantidad"] * it["precio"]
            tree.insert("", "end", values=(it["producto"], it["cantidad"], f"{it['precio']:.2f}", f"{subtotal:.2f}"))
        var_total.set(f"{calcular_total(pedido):.2f}")

    # ---- Procesar ----
    def ui_procesar():
        if not pedido:
            messagebox.showwarning("Atención", "El pedido está vacío.")
            return
        res = procesar_pedido(pedido, generar_pdf=True)
        if res["ok"]:
            messagebox.showinfo("OK", f"Venta S/ {res['total']:.2f}\nTicket: {res['formato']} ({res['ticket']})")
            pedido.clear()
            refrescar_pedido()
            refrescar_tickets()
        else:
            messagebox.showerror("Error", res.get("mensaje", "No se pudo procesar el pedido."))

    ttk.Button(frm_total, text="Procesar y Generar Ticket", command=ui_procesar).pack(side="right")

    # ---- Tickets ----
    frm_tickets = ttk.LabelFrame(root, text="Tickets recientes")
    frm_tickets.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=8, pady=8)

    lst = tk.Listbox(frm_tickets, height=8)
    lst.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    def refrescar_tickets():
        lst.delete(0, tk.END)
        for f in listar_tickets():
            lst.insert(tk.END, f)

    refrescar_tickets()

    root.mainloop()
