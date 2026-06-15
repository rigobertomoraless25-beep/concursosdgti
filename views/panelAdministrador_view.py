import flet as ft

class PanelAdministradorView(ft.Column):
    def __init__(self, page):
        self._page_ref = page
        super().__init__(
            controls=[
                ft.Text("Panel de Administrador", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("Bienvenido al panel de administracion. Aqui puedes gestionar los alumnos y disciplinas.", size=16),
                ft.ElevatedButton("Gestionar Alumnos", 
                                  icon=ft.Icons.PEOPLE, 
                                  on_click=lambda e: self._page_ref.go("/gestionar_alumno")),
                ft.ElevatedButton("Gestionar Disciplinas", 
                                  icon=ft.Icons.SCHOOL, 
                                  on_click=lambda e: self._page_ref.go("/gestionar_disciplina")),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

    