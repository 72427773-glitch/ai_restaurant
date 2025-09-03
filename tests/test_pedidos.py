import sys, os
import unittest  # 👈 AGREGA ESTA LÍNEA

# Ajustamos la ruta para que encuentre la carpeta app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.logica import agregar_producto, calcular_total, procesar_pedido

class TestPedidos(unittest.TestCase):
    def test_agregar_y_total(self):
        pedido = []
        ok, _ = agregar_producto(pedido, "Lomo Saltado", 2, 22.0)
        self.assertTrue(ok)
        ok, _ = agregar_producto(pedido, "Inka Kola 500ml", 1, 5.0)
        self.assertTrue(ok)
        self.assertAlmostEqual(calcular_total(pedido), 49.0, places=2)

    def test_procesar_pedido(self):
        pedido = []
        agregar_producto(pedido, "Ceviche Clásico", 1, 24.0)
        res = procesar_pedido(pedido, generar_pdf=False)  # usa TXT seguro
        self.assertTrue(res["ok"])
        self.assertGreater(res["total"], 0)

if __name__ == "__main__":
    unittest.main()
