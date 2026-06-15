import sqlite3

class DisciplinaDAO:
    def __init__(self):
        self.db_name = "concurso_dgeti.db"

    def insertar(self, nombre_disciplina):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO disciplinas (nombre) VALUES (?)", (nombre_disciplina,))
            conexion.commit()

    def eliminar(self, id_disciplina):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM disciplinas WHERE idDisciplina = ?", (id_disciplina,))
            conexion.commit()
    
    def modificar(self, id_disciplina, nuevo_nombre):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            # Usamos el ID para saber exactamente cuál fila actualizar
            cursor.execute("""
                UPDATE disciplinas 
                SET nombre = ? 
                WHERE idDisciplina = ?
            """, (nuevo_nombre, id_disciplina))
            conexion.commit()

    def listar_todas(self):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT idDisciplina, nombre FROM disciplinas ORDER BY nombre ASC")
            return cursor.fetchall()