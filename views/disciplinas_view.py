import flet as ft

from controllers.Disciplinas_controller import DisciplinaController


class DisciplinasView(ft.Column):
    def __init__(self, page):
        self._page_ref = page
        super().__init__(expand=True, spacing=15)

        self.controller = DisciplinaController(self)

        self.lista_disciplinas = ft.ListView(expand=True, spacing=8, padding=10)

        self.controls = [
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda _: self._page_ref.go("/"),
                        tooltip="Volver al panel",
                    ),
                    ft.Text("Gestion de Disciplinas", size=26, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.ADD,
                        tooltip="Agregar disciplina",
                        on_click=self.abrir_dialogo_agregar,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Divider(),
            ft.Text("Disciplinas registradas", size=16, weight=ft.FontWeight.W_500),
            self.lista_disciplinas,
        ]

        self.actualizar_lista_disciplinas()

    def build(self):
        return self

    def abrir_dialogo_agregar(self, e):
        txt_nombre = ft.TextField(label="Nombre de la disciplina", autofocus=True)

        def guardar(_):
            self.controller.registrar_disciplina(txt_nombre.value)
            self._cerrar_dialogo(dialogo)

        contenido = ft.Column(
            controls=[txt_nombre],
            tight=True,
        )

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Agregar Disciplina"),
            content=ft.Container(content=contenido, width=350),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self._cerrar_dialogo(dialogo)),
                ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=guardar),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._abrir_dialogo(dialogo)

    def abrir_dialogo_editar(self, id_disciplina, nombre):
        txt_nombre = ft.TextField(label="Nombre de la disciplina", value=nombre, autofocus=True)

        def guardar(_):
            self.controller.modificar_disciplina(id_disciplina, txt_nombre.value)
            self._cerrar_dialogo(dialogo)

        contenido = ft.Column(
            controls=[txt_nombre],
            tight=True,
        )

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Disciplina"),
            content=ft.Container(content=contenido, width=350),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self._cerrar_dialogo(dialogo)),
                ft.ElevatedButton("Actualizar", icon=ft.Icons.EDIT, on_click=guardar),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._abrir_dialogo(dialogo)

    def confirmar_eliminar(self, id_disciplina, nombre):
        def eliminar(_):
            self.controller.eliminar_disciplina(id_disciplina)
            self._cerrar_dialogo(dialogo)

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar disciplina"),
            content=ft.Text(f"¿Seguro que deseas eliminar '{nombre}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self._cerrar_dialogo(dialogo)),
                ft.ElevatedButton("Eliminar", icon=ft.Icons.DELETE, on_click=eliminar),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._abrir_dialogo(dialogo)

    def mostrar_mensaje(self, mensaje, es_error=False):
        self._page_ref.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor=ft.Colors.RED_700 if es_error else ft.Colors.GREEN_700,
        )
        self._page_ref.snack_bar.open = True
        self._page_ref.update()

    def limpiar_formulario_disciplina(self):
        self.actualizar_lista_disciplinas()

    def actualizar_lista_disciplinas(self):
        disciplinas = self.controller.dao.listar_todas()

        if not disciplinas:
            self.lista_disciplinas.controls = [
                ft.Container(
                    content=ft.Text("No hay disciplinas registradas."),
                    padding=10,
                )
            ]
            self._page_ref.update()
            return

        self.lista_disciplinas.controls = []
        for id_disciplina, nombre in disciplinas:
            self.lista_disciplinas.controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                expand=True,
                                controls=[
                                    ft.Text(nombre, weight=ft.FontWeight.W_600, size=16),
                                ],
                            ),
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Editar",
                                on_click=lambda _, id=id_disciplina, n=nombre: self.abrir_dialogo_editar(id, n),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Eliminar",
                                on_click=lambda _, id=id_disciplina, n=nombre: self.confirmar_eliminar(id, n),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    padding=10,
                )
            )

        self._page_ref.update()

    def _abrir_dialogo(self, dialogo):
        open_method = getattr(self._page_ref, "open", None)
        if callable(open_method):
            try:
                open_method(dialogo)
                return
            except Exception:
                pass

        show_dialog_method = getattr(self._page_ref, "show_dialog", None)
        if callable(show_dialog_method):
            try:
                show_dialog_method(dialogo)
                return
            except Exception:
                pass

        dialogo.open = True
        try:
            self._page_ref.dialog = dialogo
        except Exception:
            overlay = getattr(self._page_ref, "overlay", None)
            if overlay is not None and dialogo not in overlay:
                overlay.append(dialogo)
        self._page_ref.update()

    def _cerrar_dialogo(self, dialogo):
        close_method = getattr(self._page_ref, "close", None)
        if callable(close_method):
            try:
                close_method(dialogo)
                return
            except Exception:
                pass

        hide_dialog_method = getattr(self._page_ref, "hide_dialog", None)
        if callable(hide_dialog_method):
            try:
                hide_dialog_method()
                return
            except Exception:
                pass

        dialogo.open = False

        overlay = getattr(self._page_ref, "overlay", None)
        if overlay is not None and dialogo in overlay:
            overlay.remove(dialogo)
        
        self._page_ref.update()