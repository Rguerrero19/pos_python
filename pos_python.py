#sistema punto de venta
productos = {}
flag = True

def nuevo():
    print('Nuevo producto')
    producto = str(input('Nombre de producto: '))
    costo = float(input("Costo de producto $:"))
    categoria = str(input('Categoria de producto: '))
    productos = producto,[costo,categoria]
    print(productos)

def venta():
    v_producto = str(input('Producto en venta: '))
    if v_producto in productos:
        print('tu producto si esta')

def inventario():
    print('Inventario')

while flag is True:
    print('Funciones de menu')

    print('1.- Nueva venta','\n2.- Agregar producto nuevo','\n3.- Inventario')

    menu = int(input('Seleccione una opcion de menu: '))

    if menu == 1:
        nuevo()
    
    if menu == 2:
        nuevo()