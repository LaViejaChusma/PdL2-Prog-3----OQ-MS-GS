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
        """ En base al año de nacimiento ingresado calcula la edad (sin meses) """
        
        return (self.anio - anioNacimiento)
        
    
    
# ---------------------------------------------------------

class Persona:
    def __init__(self, nombre: str, fechaNac: Fecha, CI: int, correo: str, codigo: str):
        
        self.nombre = nombre
        self.fechaNac = fechaNac
        self.CI = CI
        self.correo = correo
        self.codigo = codigo
    
    def getNombre(self):
        return f"{self.nombre}"
    
    def getFechaNac(self):
        return f"{self.fechaNac.getFechaString}"
    
    def getCI(self):
        return f"{self.CI}"
    
    def getCorreo(self):
        return f"{self.correo}"
    
    def getCodigo(self):
        return f"{self.codigo}"
    
         # -------------- # 
         
    def setNombre(self, nombre: str):
        self.nombre = nombre
        
    def setFechaNac(self, fechaNac: Fecha):
        self.fechaNac = fechaNac
        
    def setCI(self, CI: int):
        self.CI = CI
        
    def setCorreo(self, correo: str):
        self.correo = correo
        
        
        
# ---------------------------------------------------------

class Vendedor(Persona):
    def __init__(self, nombre: str, fechaNac: Fecha, CI: int, correo: str, codigo: str,
                 productos: list, fechaIngreso: Fecha, patrimonio: float):

        # Llamado al constructor de Persona
        super().__init__(nombre, fechaNac, CI, correo, codigo)

        # Adición de atributos específicos de Vendedor
        self.productos = productos        # Lista de objetos de Producto
        self.fechaIngreso = fechaIngreso  # Un objeto de Fecha
        self.patrimonio = patrimonio      # Saldo del vendedor
        
    def getProducts(self,productos: list):
        return f"{self.productos}"
    
    def 



# ---------------------------------------------------------

class Cliente(Persona):    
    def __init__(self, nombre: str, fechaNac: Fecha, CI: int, correo: str, codigo: str,
                 carrito: list, fechaIngreso: Fecha, puntaje: int):

        super().__init__(nombre, fechaNac, CI, correo, codigo)

        self.carrito = carrito            # Lista de ítems de itemCompra
        self.fechaIngreso = fechaIngreso
        self.puntaje = puntaje



# ---------------------------------------------------------

class Compra:
    def __init__ (self, cliente: Cliente, fecha: Fecha, listado: list, modoPago: int, numeroFactura: int, codigo: str, estado: int):
        self.cliente = cliente
        self.fecha = fecha
        self.listado = listado
        self.modoPago = modoPago
        self.numeroFactura = numeroFactura
        self.codigo = codigo
        self.estado = estado
        
    def getCliente(self, cliente: Cliente):
        return f"{self.cliente}"
# ---------------------------------------------------------
#                       PROGRAMA
# ---------------------------------------------------------

f = Fecha(3, 10, 2025, 16, 30)
print(f.getFechaString())   # 03/10/2025 16:30
#f.setFecha(1, 1, 2000, 0, 0)
print(f.getFechaString())   # 01/01/2000 00:00
print(f.calcularEdad(2003))        # Probando año de nacimiento
