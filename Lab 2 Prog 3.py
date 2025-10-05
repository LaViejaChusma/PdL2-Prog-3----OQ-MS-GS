from __future__ import annotations        # <--- Debido a que algunas clases son 
                                          # interdependientes, debemos utilizar
                                          # esta librería para evitar errores cuando
                                          # hay un orden de declaración
import os

AZUL = '\033[1;34m'  # Código de escape ANSI para texto azul (color para los menús)
RESET = '\033[0m'  # Color default


# ---------------------------------------------------------
#                 CLASE FECHA
# ---------------------------------------------------------
class Fecha:
# Constructor con atributos de la clase Fecha, se declaran los tipos como int o str
    def __init__(self, dia: int, mes: int, anio: int, hora: int, minuto: int):      
        self.dia = dia       
        self.mes = mes
        self.anio = anio
        self.hora = hora
        self.minuto = minuto

    def getFechaString(self):    # Método que al ser llamado, retorna una
                                 # cadena de caracteres con datos de tiempo
        return f"{self.dia}/{self.mes}/{self.anio} → {self.hora:02d}:{self.minuto:02d}"


# ---------------------------------------------------------
#                 CLASE PRODUCTO
# ---------------------------------------------------------
class Producto:
    def __init__(self, nombre: str, fechaVenc: Fecha, provision: int, precio: float, codigo: str, marca: str):
        self.nombre = nombre
        self.fechaVenc = fechaVenc
        self.provision = provision
        self.precio = precio
        self.codigo = codigo
        self.marca = marca

    # Crea un método que muestra, en una cadena de caracteres, la información más importante del producto
    def __str__(self):             
        return f"{self.nombre} ({self.marca}) - ${self.precio} | Stock: {self.provision}"


# ---------------------------------------------------------
#                 CLASE PERSONA
# ---------------------------------------------------------
class Persona:
    def __init__(self, nombre: str, fechaNac: Fecha, CI: int, correo: str, codigo: str):
        self.nombre = nombre
        self.fechaNac = fechaNac
        self.CI = CI
        self.correo = correo
        self.codigo = codigo


# ---------------------------------------------------------
#                 CLASE VENDEDOR
# ---------------------------------------------------------
class Vendedor(Persona):
    def __init__(self, nombre: str, fechaNac: Fecha, CI: int, correo: str, codigo: str,
                 productos: list = None, fechaIngreso: Fecha = None, patrimonio: float = 0.0):
        super().__init__(nombre, fechaNac, CI, correo, codigo)  # Invoca al constructor de la
                    # superclase pertinente (Persona), para añadirle atributos adicionales
        self.productos = productos if productos is not None else []
        self.fechaIngreso = fechaIngreso
        self.patrimonio = patrimonio

    def addProducto(self, producto: Producto):  # Permite al vendedor reponer stock
        for p in self.productos:    # Bucle que busca, en base al código del producto
            if p.codigo == producto.codigo:     # su posición en la lista
                p.provision += producto.provision   # Añade la cantidad ingresada por
                                                    # el vendedor al stock del producto
                print(f"Stock actualizado: {p.nombre} → {p.provision}")
                return
        self.productos.append(producto)     # Si el producto todavía no existe, lo agrega a la lista
        print(f"Producto '{producto.nombre}' agregado al inventario.")


# ---------------------------------------------------------
#                 CLASE ITEMCOMPRA
# ---------------------------------------------------------
class ItemCompra:
    def __init__(self, producto: Producto, cantidad: int):
        self.producto = producto
        self.cantidad = cantidad
        self.subtotal = self.calcularSubtotal() # Atributo interno que toma como valor
                                                # el resultado de calcularSubtotal()

    def calcularSubtotal(self):   # Obtiene el subtotal multiplicando el precio por la cantidad
        return self.producto.precio * self.cantidad

    def __str__(self):      # Método que devuelve string de la operación subtotal
        return f"{self.cantidad}x {self.producto.nombre} → Subtotal: ${self.subtotal}"


# ---------------------------------------------------------
#                 CLASE CLIENTE
# ---------------------------------------------------------
class Cliente(Persona):     # Subclase de Persona
    def __init__(self, nombre: str, fechaNac: Fecha, CI: int, correo: str, codigo: str,
                 carrito: list = None, fechaIngreso: Fecha = None, puntaje: int = 0):
        super().__init__(nombre, fechaNac, CI, correo, codigo)  # Se le añaden atributos
        self.carrito = carrito if carrito is not None else []   # Inicializa el carrito o
                                      # con valores prestablecidos, o con una lista vacía
        
        self.fechaIngreso = fechaIngreso
        self.puntaje = puntaje

    def addAlCarrito(self, producto: Producto, cantidad: int):
        if producto.provision < cantidad:   # Chequea que haya un mayor stock que el valor
            print(f"No hay suficiente stock de {producto.nombre}.") # que se desea comprar
            return # Retorna
        item = ItemCompra(producto, cantidad)   # Asigna a un ítem su producto y cantidad
        self.carrito.append(item)       # Inserta el ítem a la lista 
        producto.provision -= cantidad  # Reduce el stock por tantas unidades como el usuario haya seleccionado
        print(f"Se agregó {cantidad}x {producto.nombre} al carrito.")

    def vaciarCarrito(self):
        self.carrito = []       # Intercambia la lista de ítems por una lista vacía

    def calcularTotal(self):
        return sum(item.subtotal for item in self.carrito)  # Calcula total de la compra


# ---------------------------------------------------------
#                 CLASE COMPRA
# ---------------------------------------------------------
class Compra:
    def __init__(self, cliente: Cliente, fecha: Fecha, listado: list, modoPago: str, numeroFactura: int, codigo: str, estado: str):
        self.cliente = cliente
        self.fecha = fecha
        self.listado = listado
        self.modoPago = modoPago
        self.numeroFactura = numeroFactura
        self.codigo = codigo
        self.estado = estado

    def mostrarListado(self): # Imprime el listado en pantalla con detalles de la compra
        print(f"\nFactura N° {self.numeroFactura} | Cliente: {self.cliente.nombre} | Estado: {self.estado}")
        print("-" * 40)       # Líneas estéticas
        for item in self.listado:   # Bucle que imprime cada ítem de la lista
            print(item)
        print("-" * 40)       # Más líneas estéticas
        print(f"Total a pagar: ${self.calcularTotal()}")

    def calcularTotal(self):
        return sum(item.subtotal for item in self.listado)  # Suma todos los subtotales de cada ítem

    def cancelarCompra(self):
        if self.estado != "Cancelada":
            for item in self.listado:
                item.producto.provision += item.cantidad  # Devuelve el stock
            self.estado = "Cancelada"
            print(f"La compra {self.numeroFactura} ha sido cancelada.")

# ---------------------------------------------------------
#                 CLASE MENU
# ---------------------------------------------------------
class Menu:
    @staticmethod     # Permite utilizar el método sin tener que crear una
    def menu():       # instancia de la clase Menu
        print(AZUL + "\n --- MENU PRINCIPAL ---" + RESET)    # Muestra el menú de color azul
        print("1 - Consultar informaciones")
        print("2 - Crear informacion")
        print("3 - Borrar informacion")
        print("4 - Nueva compra")
        print("0 - Salir")
        return input("Seleccione opción: ")     # Devuelve un valor correspondiente
                                                # a la acción deseada

    @staticmethod
    def menuConsultar():
        print(AZUL + "\n--- CONSULTAR ---" + RESET)
        print("1 - Listar clientes")
        print("2 - Listar vendedores")
        print("3 - Listar productos")
        print("4 - Listar compras")
        print("0 - Volver")
        return input("Seleccione opción: ")

# ---------------------------------------------------------
#                 FUNCIONES DE TXT
# ---------------------------------------------------------
archProductos = "dbProductos.txt"        # Crea los archivos de texto que
archClientes = "dbClientes.txt"          # almacenarán la información deseada
archVendedores = "dbVendedores.txt"
archCompras = "dbCompras.txt"


def borrarProducto():
    if not lista_productos:
        print("No hay productos para borrar.")
        return
    print("Productos disponibles:")
    for idx, p in enumerate(lista_productos):   # 
        print(f"{idx+1}. {p}")
    sel = input("Seleccione el producto a borrar (0 para cancelar): ")
    if sel == "0":
        return
    if not sel.isdigit() or int(sel) < 1 or int(sel) > len(lista_productos):
        print("Opción inválida.")
        return
    p = lista_productos.pop(int(sel)-1)
    print(f"Producto {p.nombre} borrado!")

def borrarCliente():
    if not lista_clientes:
        print("No hay clientes para borrar.")
        return
    print("Clientes disponibles:")
    for idx, c in enumerate(lista_clientes):
        print(f"{idx+1}. {c.nombre} ({c.codigo})")
    sel = input("Seleccione el cliente a borrar (0 para cancelar): ")
    if sel == "0":
        return
    if not sel.isdigit() or int(sel) < 1 or int(sel) > len(lista_clientes): # Revisa que la cadena ingresada sólamente esté compuesta de números
        print("Opción inválida.")
        return
    c = lista_clientes.pop(int(sel)-1)
    print(f"Cliente {c.nombre} borrado!")

def borrarVendedor():
    if not lista_vendedores:
        print("No hay vendedores para borrar.")
        return
    print("Vendedores disponibles:")
    for idx, v in enumerate(lista_vendedores):
        print(f"{idx+1}. {v.nombre} ({v.codigo})")
    sel = input("Seleccione el vendedor a borrar (0 para cancelar): ")
    if sel == "0":
        return
    if not sel.isdigit() or int(sel) < 1 or int(sel) > len(lista_vendedores):# Revisa acá también que la cadena ingresada sólamente esté compuesta de números
        print("Opción inválida.")
        return
    v = lista_vendedores.pop(int(sel)-1)
    print(f"Vendeor {v.nombre} borrado!")


def crearProducto():
    nombre = input("Nombre del producto: ")
    dia = int(input("Dia de vencimiento: "))
    mes = int(input("Mes de vencimiento: "))
    anio = int(input("Año de vencimiento: "))
    hora = int(input("Hora: "))
    minuto = int(input("Minuto: "))
    provision = int(input("Stock: "))
    precio = float(input("Precio: "))
    codigo = input("Código: ")
    marca = input("Marca: ")
    fecha = Fecha(dia, mes, anio, hora, minuto)
    prod = Producto(nombre, fecha, provision, precio, codigo, marca)
    lista_productos.append(prod)
    print(f"Producto {nombre} creado!")

def crearCliente():
    nombre = input("Nombre del cliente: ")
    dia = int(input("Dia de nacimiento: "))
    mes = int(input("Mes de nacimiento: "))
    anio = int(input("Año de nacimiento: "))
    hora = int(input("Hora de nacimiento: "))
    minuto = int(input("Minuto de nacimiento: "))
    CI = int(input("CI: "))
    correo = input("Correo: ")
    codigo = input("Código: ")
    fecha = Fecha(dia, mes, anio, hora, minuto)
    cliente = Cliente(nombre, fecha, CI, correo, codigo)
    lista_clientes.append(cliente)
    print(f"Cliente {nombre} creado!")

def crearVendedor():
    nombre = input("Nombre del vendedor: ")
    dia = int(input("Dia de nacimiento: "))
    mes = int(input("Mes de nacimiento: "))
    anio = int(input("Año de nacimiento: "))
    hora = int(input("Hora de nacimiento: "))
    minuto = int(input("Minuto de nacimiento: "))
    CI = int(input("CI: "))
    correo = input("Correo: ")
    codigo = input("Código: ")
    patrimonio = float(input("Patrimonio inicial: "))
    fecha = Fecha(dia, mes, anio, hora, minuto)
    vendedor = Vendedor(nombre, fecha, CI, correo, codigo, [], fecha, patrimonio)
    lista_vendedores.append(vendedor)
    print(f"Vendedor {nombre} creado!")


def guardar_productos(lista_productos):     # Método para manejar carpetas
    with open(archProductos, "w") as f:     
        for p in lista_productos:           # Por cada producto, ingresa en el archivo de texto toda su información pertinente
            f.write(f"{p.nombre},{p.fechaVenc.dia},{p.fechaVenc.mes},{p.fechaVenc.anio},{p.fechaVenc.hora},{p.fechaVenc.minuto},{p.provision},{p.precio},{p.codigo},{p.marca}\n")

def guardar_clientes(lista_clientes):
    with open(archClientes, "w") as f:
        for c in lista_clientes:
            f.write(f"{c.nombre},{c.fechaNac.dia},{c.fechaNac.mes},{c.fechaNac.anio},{c.fechaNac.hora},{c.fechaNac.minuto},{c.CI},{c.correo},{c.codigo}\n")

def guardar_vendedores(lista_vendedores):
    with open(archVendedores, "w") as f:
        for v in lista_vendedores:
            f.write(f"{v.nombre},{v.fechaNac.dia},{v.fechaNac.mes},{v.fechaNac.anio},{v.fechaNac.hora},{v.fechaNac.minuto},{v.CI},{v.correo},{v.codigo},{v.patrimonio}\n")

def guardar_compras(lista_compras):
    with open(archCompras, "w") as f:
        for comp in lista_compras:
            items = ";".join([f"{item.producto.codigo}:{item.cantidad}" for item in comp.listado])
            f.write(f"{comp.cliente.codigo},{comp.fecha.dia},{comp.fecha.mes},{comp.fecha.anio},{comp.fecha.hora},{comp.fecha.minuto},{comp.numeroFactura},{comp.codigo},{comp.estado},{items}\n")

def cargar_productos():
    productos = []
    if not os.path.exists(archProductos):
        return productos
    with open(archProductos) as f:
        for line in f:
            parts = line.strip().split(",")
            fecha = Fecha(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5]))
            p = Producto(parts[0], fecha, int(parts[6]), float(parts[7]), parts[8], parts[9])
            productos.append(p)
    return productos

def cargar_clientes():
    clientes = []
    if not os.path.exists(archClientes):
        return clientes
    with open(archClientes) as f:
        for line in f:
            parts = line.strip().split(",")
            fecha = Fecha(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5]))
            c = Cliente(parts[0], fecha, int(parts[6]), parts[7], parts[8])
            clientes.append(c)
    return clientes

def cargar_vendedores():
    vendedores = []
    if not os.path.exists(archVendedores):
        return vendedores
    with open(archVendedores) as f:
        for line in f:
            parts = line.strip().split(",")
            fecha = Fecha(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5]))
            v = Vendedor(parts[0], fecha, int(parts[6]), parts[7], parts[8], [], fecha, float(parts[9]))
            vendedores.append(v)
    return vendedores

# ---------------------------------------------------------
#                 PROGRAMA PRINCIPAL
# ---------------------------------------------------------
if __name__ == "__main__":
    # Cargar datos de archivos
    lista_productos = cargar_productos()
    lista_clientes = cargar_clientes()
    lista_vendedores = cargar_vendedores()
    lista_compras = []

    # Datos de ejemplo si listas arrancan vacías
    hoy = Fecha(3, 10, 2025, 16, 30)
    if not lista_productos:
        p1 = Producto("Leche", hoy, 10, 120, "A1", "Conaprole")
        p2 = Producto("Café", hoy, 5, 250, "A2", "LaVirginia")
        lista_productos.extend([p1, p2])
    if not lista_vendedores:
        v1 = Vendedor("Oscar", hoy, 12345678, "oscar@correo.com", "V001")
        v1.addProducto(lista_productos[0])
        v1.addProducto(lista_productos[1])
        lista_vendedores.append(v1)
    if not lista_clientes:
        c1 = Cliente("Mateo", hoy, 87654321, "mateo@correo.com", "C001")
        lista_clientes.append(c1)

    # Menu principal
    while True:
        op = Menu.menu()

        if op == "1":  # Consultar
            opc = Menu.menuConsultar()
            if opc == "1":
                print("\nClientes:")
                for c in lista_clientes:
                    print(f"{c.nombre} ({c.codigo})")
            elif opc == "2":
                print("\nVendedores:")
                for v in lista_vendedores:
                    print(f"{v.nombre} ({v.codigo})")
            elif opc == "3":
                print("\nProductos:")
                for p in lista_productos:
                    print(p)
            elif opc == "4":
                print("\nCompras:")
                for comp in lista_compras:
                    comp.mostrarListado()
                    
        elif op == "2":  # Crear informacion
            print("\n--- CREAR INFORMACION ---")
            print("1 - Crear cliente")
            print("2 - Crear vendedor")
            print("3 - Crear producto")
            print("0 - Volver")
            choice = input("Seleccione opción: ")
            if choice == "1":
                crearCliente()
            elif choice == "2":
                crearVendedor()
            elif choice == "3":
                crearProducto()
                
        elif op == "3":  # Borrar informacion
            print(AZUL + "\n--- BORRAR INFORMACION ---" + RESET)
            print("1 - Borrar cliente")
            print("2 - Borrar vendedor")
            print("3 - Borrar producto")
            print("0 - Volver")
            choice = input("Seleccione opción: ")
            if choice == "1":
                borrarCliente()
            elif choice == "2":
                borrarVendedor()
            elif choice == "3":
                borrarProducto()



        elif op == "4":  # Nueva compra interactiva
            if not lista_clientes or not lista_productos:
                print("Faltan clientes o productos.")
                continue

            cliente = lista_clientes[0]
            print(f"\nCliente seleccionado: {cliente.nombre}")

            while True:
                print("\nProductos disponibles:")
                for idx, p in enumerate(lista_productos):
                    print(f"{idx+1}. {p} ")
                prod_sel = input("Seleccione el producto (0 para terminar): ")
                if prod_sel == "0":
                    break
                if not prod_sel.isdigit() or int(prod_sel) < 1 or int(prod_sel) > len(lista_productos):
                    print("Opción inválida.")
                    continue
                prod_idx = int(prod_sel) - 1
                cantidad = input(f"Ingrese cantidad para {lista_productos[prod_idx].nombre}: ")
                if not cantidad.isdigit() or int(cantidad) < 1:
                    print("Cantidad inválida.")
                    continue
                cliente.addAlCarrito(lista_productos[prod_idx], int(cantidad))

            if cliente.carrito:
                compra = Compra(cliente, hoy, cliente.carrito, "Efectivo",
                                len(lista_compras) + 1, f"C{len(lista_compras)+1}", "Completada")
                lista_compras.append(compra)
                compra.mostrarListado()
                cliente.vaciarCarrito()
            else:
                print("No se realizó ninguna compra.")

        elif op == "0":
            # Guardar todo antes de salir
            guardar_productos(lista_productos)
            guardar_clientes(lista_clientes)
            guardar_vendedores(lista_vendedores)
            guardar_compras(lista_compras)
            print('\033[1;32m' + "Datos guardados. Saliendo del programa..." + '\033[0m')
            break
