#sistema punto de venta
productos = {}
flag = True
#hola como estas
def nuevo():
    print('Nuevo producto')
    nombre = str(input('Nombre de producto: '))
    costo = float(input("Costo de producto $:"))
    cantidad = int(input('Cantidad inicial de este producto: '))
    categoria = str(input('Categoria de producto: '))
    productos [nombre] = [costo,cantidad,categoria]
    print(productos)

def venta():
    print("Elegiste vender un producto")
    

def inventario():#funcion a mejorar
    prod_inventario = str(input('Nombre de producto encontrado: '))
    if prod_inventario in productos:
        contado = []
        suma = 0
        while contado != cantidad:
            print('te faltan')

while flag is True:
    print('Funciones de menu')

    print('1.- Agregar producto','\n2.- Venta de producto','\n3.- Inventario')

    menu = int(input('Seleccione una opcion de menu: '))

    if menu == 1:
        nuevo()
    
    elif menu == 2:
        venta()
    
    elif menu == 3:
        inventario()
