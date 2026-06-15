
import sqlite3

def crear_tablas():
    conexion = sqlite3.connect("concurso_dgeti.db")
    cursor = conexion.cursor()
    
    # Tabla de Disciplinas (El ID se genera solo)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disciplinas (
            idDisciplina INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
    """)
    
    # Tabla de Alumnos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alumnos (
            idAlumno INTEGER PRIMARY KEY AUTOINCREMENT,       
            matricula TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            nss TEXT NOT NULL,
            plantel TEXT NOT NULL,
            calificacion INTEGER,
            id_disciplina INTEGER,
            FOREIGN KEY (id_disciplina) REFERENCES disciplinas (idDisciplina)
        )
    """)
    
    conexion.commit()
    conexion.close()