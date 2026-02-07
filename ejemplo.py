products={}
flag=True

while True:
  print('''
    1. Añadir productos.
    2. Buscar producto.
    3. Inventario.
    4. Ver productos.
    5. Venta
    6. Compra''')
  
  respuesta=int(input('Ingrese su opcion: '))
  
  if respuesta == 1:
    print('\t Agregar producto nuevo')
    name=str(input('Nombre de el producto: '))
    code=int(input('Codigo de producto: '))
    quantity=int(input('Cantidad de producto: '))
    coste=float(input('Precio de venta :$'))
    products [name]=[code,quantity,coste]
    print(products)
  elif respuesta == 2:
    search=str(input('Nombre del producto a buscar: '))
    if search in products:
      print(f'Detalles de producto {products[search]}')
  elif respuesta ==3:
    search=str(input('Producto a inventariar: '))
    if search in products:
      contado=[]
      suma=0
      while contado != quantity:
        print('Digita 0 para terminar en cualquier momento')
        encontrado=int(input('Cantidad encontrada: '))
        contado.append(encontrado)
        print(f'Has encontrado {contado}')
        for i in contado:
          suma=sum(contado)
        print(f'Total encontrado {suma}')
        if encontrado == 0:
          print(f'Total encontrado {suma}')
          print(f'Valor de inventario {suma*coste}')
          break
        if suma>=quantity:
          terminar=str(input('A encotrado todos los productos deceas terminar (y/n): '))
          if terminar=='y':
            print(f'valor de inventario {suma*coste}')
            break
    else:
      print(f'El producto {search} no se encuentra en tu inventario')
  elif respuesta == 4:
    for i in products:
      print(products[i])
  elif respuesta == 5:
    venta=(str(input('Producto a vender: ')))
    print(f'Estas vendiendo {venta}')
    if venta in products:
      cantidad=int(input('Cantidad a vender: '))
      if cantidad<=quantity:
        quantity= quantity-cantidad
        products [venta][1] = quantity
        print(f'Has vendido {venta}')
        print(f'Haora cuentas con {quantity} pz')
      else:
        print('No cuentas con la cantidad suficiente para la venta de este produnto')
  elif respuesta == 6:
    print('Comprar producto')
    compra=str(input('Producto a comprar: '))
    if compra in products:
      cantidad=int(input('Cantidad a comprar: '))
      quantity=quantity+cantidad
      products [compra][1]=quantity
      print(f'Ahora cuentas con {quantity} de {compra}')


        cajero
'''Hacer uan jejercicio que simule  un cajero automatico 
con las siguientes opciones:
1.Ingresar dinero
2.Retirar dinero
3.Mostrar saldo disponible
4.Salir'''

saldo=1000
print('\t MENU')
print('1.Hacer depocito...')
print('2.Retirar dinero de la cuenta...')
print('3.Mostrar saldo disponible...')
print('4.Salir...')
opcion= int(input('Digite una opcion de menu:'))

if opcion==1:
    depocito=float(input('Cantidad a ingresar: $'))
    saldo += depocito
    print(f'Tu nuevo saldo es de: {saldo}')
elif opcion==2:
    retirar=float(input('Cuanrto dinero decea retirar: $'))
    if retirar<=saldo:
        saldo-=retirar
        print(f'Tu nuevo saldo es: ${saldo}')
    else:
        print('No cuetas con saldo suficiente en tu cuenta')
elif opcion==3:
    print(f'Tu saldo es de ${saldo}')
elif opcion==4:
    print('GRacias por su preferencia')
else:
    print('Seleccione una opcion de menu:')
    