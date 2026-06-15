# controllers/disciplina_controller.py
from models.Disciplinas_dao import DisciplinaDAO

class DisciplinaController:
    def __init__(self, vista):
        # Guardamos una referencia a la vista para poder enviarle respuestas (mensajes de éxito o error)
        self.vista = vista
        # Creamos una instancia de nuestro DAO para comunicarnos con la base de datos
        self.dao = DisciplinaDAO()


    #función para registrar una disciplina, recibe el nombre de la disciplina a registrar
    def registrar_disciplina(self, nombre):
        """Lógica de negocio y control para dar de alta una disciplina"""
        # Validación simple de lógica de negocio: ¡que el nombre no esté vacío o lleno de espacios!
        if not nombre or nombre.strip() == "":
            self.vista.mostrar_mensaje("Error: El nombre de la disciplina no puede estar vacío.", es_error=True)
            return

        try:
            # Si todo está bien, llamamos al modelo para insertar
            self.dao.insertar(nombre.strip())
            self.vista.mostrar_mensaje(f"¡Disciplina '{nombre}' registrada con éxito!")
            self.vista.limpiar_formulario_disciplina() # Le pedimos a la vista que limpie su caja de texto
        except Exception as e:
            self.vista.mostrar_mensaje(f"Error al guardar en la base de datos: {e}", es_error=True)
   
   
    #funcion para modificar una disciplina, recibe el id de la disciplina a modificar y el nuevo nombre que se le quiere asignar
    def modificar_disciplina(self, id_disciplina, nuevo_nombre):
        """Lógica para actualizar el nombre de una disciplina"""
        if not nuevo_nombre or nuevo_nombre.strip() == "":
            self.vista.mostrar_mensaje("Error: El nuevo nombre no puede estar vacío.", es_error=True)
            return

        try:
            self.dao.modificar(id_disciplina, nuevo_nombre.strip())
            self.vista.mostrar_mensaje("¡Disciplina actualizada correctamente!")
            self.vista.actualizar_lista_disciplinas() # Le dice a la vista que refresque la pantalla
        except Exception as e:
            self.vista.mostrar_mensaje(f"Error al modificar: {e}", es_error=True)

    #función para eliminar una disciplina, recibe el id de la disciplina a eliminar
    def eliminar_disciplina(self, id_disciplina):
        """Lógica para eliminar una disciplina por su ID"""
        try:
            # Aquí va nuestra regla de negocio: mandamos a borrar al DAO
            self.dao.eliminar(id_disciplina)
            self.vista.mostrar_mensaje("¡Disciplina eliminada con éxito!")
            self.vista.actualizar_lista_disciplinas()
        except Exception as e:
            self.vista.mostrar_mensaje(f"Error al eliminar: {e}", es_error=True)