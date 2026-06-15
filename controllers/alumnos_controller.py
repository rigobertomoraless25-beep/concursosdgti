from models.Alumnos_dao import AlumnoDAO
from models.Alumnos import Alumno
from models.Disciplina import Disciplina
from models.Disciplinas_dao import DisciplinaDAO


class AlumnosController:
    def __init__(self, vista):
        self.vista = vista
        self.dao = AlumnoDAO()
        self.disciplinas_dao = DisciplinaDAO()

    def obtener_disciplinas(self):
        return self.disciplinas_dao.listar_todas()

    def _crear_disciplina(self, id_disciplina):
        return Disciplina(nombre="", idDisciplina=int(id_disciplina))

    def listar_alumnos(self, id_disciplina=None):
        if id_disciplina in (None, "", "todas"):
            return self.dao.listar_todos()

        try:
            return self.dao.listar_por_disciplina(int(id_disciplina))
        except (TypeError, ValueError):
            return self.dao.listar_todos()

    def registrar_alumno(self, nombre, matricula, nss, plantel, calificacion, disciplina):
        if not nombre or nombre.strip() == "" or not matricula or matricula.strip() == "" or not nss or nss.strip() == "" or not plantel or plantel.strip() == "" or calificacion is None or disciplina is None:
            self.vista.mostrar_mensaje("Error: Todos los campos son obligatorios.", es_error=True)
            return
        try:
            calificacion_num = int(calificacion)
            disciplina_obj = self._crear_disciplina(disciplina)
        except (TypeError, ValueError):
            self.vista.mostrar_mensaje("Error: Calificación o disciplina inválidas.", es_error=True)
            return

        alumno_objeto = Alumno(
            matricula=matricula.strip(),
            nombre=nombre.strip(),
            nss=nss.strip(),
            plantel=plantel.strip(),
            calificacion=calificacion_num,
            disciplina=disciplina_obj,
        )
        try:

            self.dao.insertar(alumno_objeto)
            self.vista.mostrar_mensaje(f"¡Alumno registrado con éxito!")
            self.vista.limpiar_formulario_alumno()
        except Exception as e:
            self.vista.mostrar_mensaje(f"Error al guardar en la base de datos: {e}", es_error=True)

    def modificar_alumno(self, id_alumno, nombre,matricula, nss, plantel, calificacion, disciplina):
        if not nombre or not matricula or not nss or not plantel or calificacion is None or disciplina is None:
            self.vista.mostrar_mensaje("Error: Todos los campos son obligatorios.", es_error=True)
            return

        try:
            calificacion_num = int(calificacion)
            disciplina_obj = self._crear_disciplina(disciplina)
        except (TypeError, ValueError):
            self.vista.mostrar_mensaje("Error: Calificación o disciplina inválidas.", es_error=True)
            return
        
        alumno_objeto = Alumno(
            matricula=matricula.strip(),
            nombre=nombre.strip(),
            nss=nss.strip(),
            plantel=plantel.strip(),
            calificacion=calificacion_num,
            disciplina=disciplina_obj,
        )    

        try:
            self.dao.modificar(alumno_objeto)
            self.vista.mostrar_mensaje("¡Alumno actualizado correctamente!")
            self.vista.actualizar_lista_alumnos()
        except Exception as e:
            self.vista.mostrar_mensaje(f"Error al modificar: {e}", es_error=True)

    def eliminar_alumno(self, matricula):
        try:
            self.dao.eliminar(matricula)
            self.vista.mostrar_mensaje("¡Alumno eliminado con éxito!")
            self.vista.actualizar_lista_alumnos()
        except Exception as e:
            self.vista.mostrar_mensaje(f"Error al eliminar: {e}", es_error=True)