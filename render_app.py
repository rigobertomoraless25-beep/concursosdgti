from main import main, crear_tablas
import flet

# Crear las tablas de la base de datos antes de levantar la app web
crear_tablas()

# Exportar la app Flet como ASGI compatible con uvicorn/Render
app = flet.run(main, export_asgi_app=True)
