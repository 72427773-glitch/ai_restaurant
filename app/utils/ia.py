import random

SUGERENCIAS = [
    "Ceviche Clásico",
    "Lomo Saltado",
    "Aji de Gallina",
    "Pollo a la Brasa",
    "Arroz con Mariscos",
    "Anticuchos",
    "Papa a la Huancaína",
    "Tallarin Saltado",
]

def sugerir_platillos(n=3):
    n = max(1, min(n, len(SUGERENCIAS)))
    return random.sample(SUGERENCIAS, n)
