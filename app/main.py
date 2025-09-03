# Punto de entrada
try:
    from app.interfaz import iniciar_app
except Exception:
    from interfaz import iniciar_app

if __name__ == "__main__":
    iniciar_app()
