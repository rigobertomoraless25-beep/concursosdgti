class Alumno:
    def __init__(self, nombre, matricula,nss,plantel,calificacion,disciplina):
        self.nombre = nombre
        self.matricula = matricula
        self.nss = nss
        self.plantel = plantel

        #Logica del negocio, verificamos que esté dentro del rango permitido (5 a 10)
        if calificacion < 5 or calificacion > 10:
            raise ValueError("La calificación debe estar entre 5 y 10.")
        else:
            self.calificacion = calificacion

        self.disciplina = disciplina

    #devuelve una representación legible del objeto Alumno, mostrando sus atributos principales
    def __str__(self):
        return f"Alumno: {self.nombre}, Matricula: {self.matricula}, NSS: {self.nss}, Plantel: {self.plantel}, Calificacion: {self.calificacion}, Disciplina: {self.disciplina}"