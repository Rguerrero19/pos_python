#sistema punto de venta
productos = {}
flag = True

def venta():
    print("Elegiste vender un producto")
    vender = str(input('Selecciona un producto: '))
    if vender in productos:
        venta = int(input('Cantidad a vender: '))
        productos[vender][1] -= venta #funcion a mejorar
        print(productos)
    else:
        print('El producto no se encuentra en tu inventario')

def nuevo():
    print('Nuevo producto')
    nombre = str(input('Nombre de producto: '))
    costo = float(input("Costo de producto $:"))
    cantidad = int(input('Cantidad inicial de este producto: '))
    categoria = str(input('Categoria de producto: '))
    productos [nombre] = [costo,cantidad,categoria]
    print(productos)

def inventario():
    print("Elegiste realizar un inventario")
    cat_inventario = str(input('Seleccione una categoria a inventariar: '))
    if cat_inventario in (productos[categoria]):
        print('tu categoria si esta en el  inventario')
    else:
        print('La categoria seleccionada no se encuentra')

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