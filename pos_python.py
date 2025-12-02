#sistema punto de venta
productos = {}
flag = True

def venta():
    print("Elegiste vender un producto")
    vender = str(input('Selecciona un producto: '))
    if vender in productos:
        print(productos)
    else:
        print('El producto no se encuentra en tu inventario')

def nuevo():
    print('Nuevo producto')
    nombre = str(input('Nombre de producto: '))
    costo = float(input("Costo de producto $:"))
    categoria = str(input('Categoria de producto: '))
    productos = nombre,[costo,categoria]
    print(productos)

def inventario():
    print("Elegiste realizar un inventario")

while flag is True:
    print('Funciones de menu')

    print('1.- Nueva venta','\n2.- Agregar producto nuevo','\n3.- Inventario')

    menu = int(input('Seleccione una opcion de menu: '))

    if menu == 1:
        venta()
    
    elif menu == 2:
        nuevo()
    
    elif menu == 3:
        inventario()