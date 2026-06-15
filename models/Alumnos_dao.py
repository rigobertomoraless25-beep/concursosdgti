# models/alumno_dao.py
import sqlite3

class AlumnoDAO:
    def __init__(self):
        self.db_name = "concurso_dgeti.db"

    def _obtener_id_disciplina(self, disciplina):
        return getattr(disciplina, "id_disciplina", getattr(disciplina, "idDisciplina", None))

    def insertar(self, alumno_objeto):
        """Recibe un objeto de la clase Alumno y lo guarda en la BD"""
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("""
                    INSERT INTO alumnos (matricula, nombre, nss, plantel, calificacion, id_disciplina)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    alumno_objeto.matricula,
                    alumno_objeto.nombre,
                    alumno_objeto.nss,
                    alumno_objeto.plantel,
                    alumno_objeto.calificacion,
                    self._obtener_id_disciplina(alumno_objeto.disciplina)
                ))
                conexion.commit()
            except sqlite3.IntegrityError:
                # Si la matrícula ya existe, lanzamos un error de lógica de negocio
                raise ValueError("La matrícula ya se encuentra registrada en el sistema.")

    def modificar(self, alumno_objeto):
        """Recibe un objeto Alumno con datos actualizados y lo guarda usando su matrícula"""
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE alumnos 
                SET nombre = ?, nss = ?, plantel = ?, calificacion = ?, id_disciplina = ?
                WHERE matricula = ?
            """, (
                alumno_objeto.nombre,
                alumno_objeto.nss,
                alumno_objeto.plantel,
                alumno_objeto.calificacion,
                self._obtener_id_disciplina(alumno_objeto.disciplina),
                alumno_objeto.matricula  # Condición clave para saber a quién modificar
            ))
            conexion.commit()

    def eliminar(self, matricula):
        """Elimina a un alumno usando su matrícula como identificador único"""
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM alumnos WHERE matricula = ?", (matricula,))
            conexion.commit()

    def listar_todos(self):
        """Devuelve una lista de tuplas con los datos de todos los alumnos registrados"""
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT a.matricula, a.nombre, a.nss, a.plantel, a.calificacion, d.idDisciplina, d.nombre
                FROM alumnos a
                LEFT JOIN disciplinas d ON a.id_disciplina = d.idDisciplina
                ORDER BY a.nombre ASC
            """)
            return cursor.fetchall()

    def listar_por_disciplina(self, id_disciplina):
        """Devuelve alumnos filtrados por disciplina"""
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                """
                SELECT a.matricula, a.nombre, a.nss, a.plantel, a.calificacion, d.idDisciplina, d.nombre
                FROM alumnos a
                LEFT JOIN disciplinas d ON a.id_disciplina = d.idDisciplina
                WHERE a.id_disciplina = ?
                ORDER BY a.nombre ASC
                """,
                (id_disciplina,),
            )
            return cursor.fetchall()