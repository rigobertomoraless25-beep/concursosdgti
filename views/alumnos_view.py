import flet as ft

from controllers.alumnos_controller import AlumnosController


class AlumnosView(ft.Column):
	def __init__(self, page):
		self._page_ref = page
		super().__init__(expand=True, spacing=15)

		self.controller = AlumnosController(self)

		self.lista_alumnos = ft.ListView(expand=True, spacing=8, padding=10)
		self.filtro_disciplina = ft.Dropdown(
			label="Filtrar por disciplina",
			value="todas",
			helper_text="Selecciona una disciplina para filtrar",
			width=320,
		)
		self.filtro_disciplina.on_change = lambda _: self.actualizar_lista_alumnos()
		self._actualizar_opciones_filtro()

		self.controls = [
			ft.Row(
				controls=[
					ft.IconButton(
						icon=ft.Icons.ARROW_BACK,
						on_click=lambda _: self._page_ref.go("/"),
						tooltip="Volver al panel",
					),
					ft.Text("Gestion de Alumnos", size=26, weight=ft.FontWeight.BOLD),
					ft.Container(expand=True),
					ft.IconButton(
						icon=ft.Icons.ADD,
						tooltip="Agregar alumno",
						on_click=self.abrir_dialogo_agregar,
					),
				],
				alignment=ft.MainAxisAlignment.START,
				vertical_alignment=ft.CrossAxisAlignment.CENTER,
			),
			ft.Divider(),
			self.filtro_disciplina,
			ft.Text("Alumnos registrados", size=16, weight=ft.FontWeight.W_500),
			self.lista_alumnos,
		]

		self.actualizar_lista_alumnos()

	def build(self):
		return self

	def _crear_opciones_disciplinas(self):
		disciplinas = self.controller.obtener_disciplinas()
		return [ft.dropdown.Option(str(id_disciplina), nombre) for id_disciplina, nombre in disciplinas]

	def _actualizar_opciones_filtro(self):
		opciones = [ft.dropdown.Option("todas", "Todas las disciplinas")]
		opciones.extend(self._crear_opciones_disciplinas())
		self.filtro_disciplina.options = opciones

		if not self.filtro_disciplina.value:
			self.filtro_disciplina.value = "todas"

	def abrir_dialogo_agregar(self, e):
		opciones_disciplinas = self._crear_opciones_disciplinas()

		txt_nombre = ft.TextField(label="Nombre", autofocus=True)
		txt_matricula = ft.TextField(label="Matricula")
		txt_nss = ft.TextField(label="NSS")
		txt_plantel = ft.TextField(label="Plantel")
		txt_calificacion = ft.TextField(label="Calificacion", keyboard_type=ft.KeyboardType.NUMBER)
		cb_disciplina = ft.Dropdown(
			label="Disciplina",
			options=opciones_disciplinas,
			hint_text="Seleccione una disciplina",
		)

		def guardar(_):
			self.controller.registrar_alumno(
				txt_nombre.value,
				txt_matricula.value,
				txt_nss.value,
				txt_plantel.value,
				txt_calificacion.value,
				cb_disciplina.value,
			)
			self._cerrar_dialogo(dialogo)

		contenido = ft.Column(
			controls=[
				txt_nombre,
				txt_matricula,
				txt_nss,
				txt_plantel,
				txt_calificacion,
				cb_disciplina,
			],
			tight=True,
			scroll=ft.ScrollMode.AUTO,
		)

		dialogo = ft.AlertDialog(
			modal=True,
			title=ft.Text("Agregar alumno"),
			content=ft.Container(content=contenido, width=420),
			actions=[
				ft.TextButton("Cancelar", on_click=lambda _: self._cerrar_dialogo(dialogo)),
				ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=guardar),
			],
			actions_alignment=ft.MainAxisAlignment.END,
		)
		self._abrir_dialogo(dialogo)

	def abrir_dialogo_editar(self, alumno):
		matricula, nombre, nss, plantel, calificacion, id_disciplina, _ = alumno
		opciones_disciplinas = self._crear_opciones_disciplinas()

		txt_nombre = ft.TextField(label="Nombre", value=nombre, autofocus=True)
		txt_matricula = ft.TextField(label="Matricula", value=matricula, disabled=True)
		txt_nss = ft.TextField(label="NSS", value=nss)
		txt_plantel = ft.TextField(label="Plantel", value=plantel)
		txt_calificacion = ft.TextField(
			label="Calificacion",
			value="" if calificacion is None else str(calificacion),
			keyboard_type=ft.KeyboardType.NUMBER,
		)
		cb_disciplina = ft.Dropdown(
			label="Disciplina",
			value="" if id_disciplina is None else str(id_disciplina),
			options=opciones_disciplinas,
			hint_text="Seleccione una disciplina",
		)

		def guardar(_):
			self.controller.modificar_alumno(
				None,
				txt_nombre.value,
				txt_matricula.value,
				txt_nss.value,
				txt_plantel.value,
				txt_calificacion.value,
				cb_disciplina.value,
			)
			self._cerrar_dialogo(dialogo)

		contenido = ft.Column(
			controls=[
				txt_nombre,
				txt_matricula,
				txt_nss,
				txt_plantel,
				txt_calificacion,
				cb_disciplina,
			],
			tight=True,
			scroll=ft.ScrollMode.AUTO,
		)

		dialogo = ft.AlertDialog(
			modal=True,
			title=ft.Text("Editar alumno"),
			content=ft.Container(content=contenido, width=420),
			actions=[
				ft.TextButton("Cancelar", on_click=lambda _: self._cerrar_dialogo(dialogo)),
				ft.ElevatedButton("Actualizar", icon=ft.Icons.EDIT, on_click=guardar),
			],
			actions_alignment=ft.MainAxisAlignment.END,
		)
		self._abrir_dialogo(dialogo)

	def confirmar_eliminar(self, matricula, nombre):
		def eliminar(_):
			self.controller.eliminar_alumno(matricula)
			self._cerrar_dialogo(dialogo)

		dialogo = ft.AlertDialog(
			modal=True,
			title=ft.Text("Eliminar alumno"),
			content=ft.Text(f"¿Seguro que deseas eliminar a '{nombre}'?"),
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

	def limpiar_formulario_alumno(self):
		self.actualizar_lista_alumnos()

	def actualizar_lista_alumnos(self):
		self._actualizar_opciones_filtro()
		alumnos = self.controller.listar_alumnos(self.filtro_disciplina.value)

		if not alumnos:
			self.lista_alumnos.controls = [
				ft.Container(
					content=ft.Text("No hay alumnos registrados."),
					padding=10,
				)
			]
			self._page_ref.update()
			return

		self.lista_alumnos.controls = []
		for alumno in alumnos:
			matricula, nombre, nss, plantel, calificacion, _, nombre_disciplina = alumno
			subtitulo = f"Matricula: {matricula} | NSS: {nss} | Plantel: {plantel} | Calificacion: {calificacion} | Disciplina: {nombre_disciplina or 'Sin asignar'}"

			self.lista_alumnos.controls.append(
				ft.Container(
					content=ft.Row(
						controls=[
							ft.Column(
								expand=True,
								controls=[
									ft.Text(nombre, weight=ft.FontWeight.W_600),
									ft.Text(subtitulo, size=12, color=ft.Colors.BLACK54),
								],
							),
							ft.IconButton(
								icon=ft.Icons.EDIT,
								tooltip="Editar",
								on_click=lambda _, a=alumno: self.abrir_dialogo_editar(a),
							),
							ft.IconButton(
								icon=ft.Icons.DELETE,
								tooltip="Eliminar",
								on_click=lambda _, m=matricula, n=nombre: self.confirmar_eliminar(m, n),
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