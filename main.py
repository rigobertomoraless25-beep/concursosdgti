import flet as ft

from views.panelAdministrador_view import PanelAdministradorView
from views.alumnos_view import AlumnosView
from views.disciplinas_view import DisciplinasView
from models.dataBase import crear_tablas

def main(page: ft.Page):
    page.title = "App Concurso Cívico - DGETI"
    page.window_width = 800
    page.window_height = 600
    # Tema institucional DGETI (guinda principal tomado del sitio de referencia)
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed="#611232")
    page.bgcolor = "#F7F4EF"

    

    def route_change(e):
        ruta = page.route
        print(f"--- DISPARANDO RUTEADOR: {ruta} ---")
        
        # Limpiamos las vistas en el stack para una SPA óptima
        page.views.clear()

        # 1. Tu ruta principal que carga el panel que creaste
        if ruta == "/":
            page.views.append(
                ft.View(
                    route="/",
                    controls=[PanelAdministradorView(page)],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        
        # 2. Ruta para gestionar alumnos
        if ruta == "/gestionar_alumno":
            page.views.append(
                ft.View(
                    route="/gestionar_alumno",
                    controls=[AlumnosView(page)],
                    padding=20,
                    scroll=ft.ScrollMode.AUTO,
                )
            )
            
        # 3. Ruta para gestionar disciplinas
        if ruta == "/gestionar_disciplina":
            page.views.append(
                ft.View(
                    route="/gestionar_disciplina",
                    controls=[DisciplinasView(page)],
                    padding=20,
                    scroll=ft.ScrollMode.AUTO,
                )
            )
        
        page.update()

    # Asignamos el evento del ruteador
    page.on_route_change = route_change

    # Aseguramos la ruta raíz por defecto
    if not page.route:
        page.route = "/"

    # Forzamos la ejecución manual la primera vez
    route_change(None)

if __name__ == "__main__":
    crear_tablas()
    ft.app(target=main)