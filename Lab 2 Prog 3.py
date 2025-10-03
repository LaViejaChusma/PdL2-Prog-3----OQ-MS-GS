import math
import time


# ---------------------------------------------------------
#                 Creación de clases
# ---------------------------------------------------------

class Fecha:
    def __init__(self, dia: int, mes: int, anio: int, hora: int, minuto: int):
        self.dia = dia
        self.mes = mes
        self.anio = anio
        self.hora = hora
        self.minuto = minuto

    def setFecha(self, dia: int, mes: int, anio: int, hora: int, minuto: int):
        """ Actualiza la fecha y hora """
        
        self.dia = dia
        self.mes = mes
        self.anio = anio
        self.hora = hora
        self.minuto = minuto
        
    def getFechaString(self):
        """ Devuelve una cadena con los valores de Fecha relacionados """
        
        return f"{self.dia}/{self.mes}/{self.anio} --> {self.hora}:{self.minuto}"
    
    def calcularEdad(self,anioNacimiento: int):
        
        return (self.anio - anioNacimiento)
        
    
# ---------------------------------------------------------
#                       PROGRAMA
# ---------------------------------------------------------

f = Fecha(3, 10, 2025, 16, 30)
print(f.getFechaString())   # 03/10/2025 16:30
#f.setFecha(1, 1, 2000, 0, 0)
print(f.getFechaString())   # 01/01/2000 00:00
print(f.calcularEdad(2003))        # Probando año de nacimiento
