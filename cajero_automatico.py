"""
Cajero Automático Simulator
Ejercicio que simula un cajero automático con las siguientes opciones:
1. Ingresar dinero (Depósito)
2. Retirar dinero
3. Mostrar saldo disponible
4. Salir
"""

saldo = 1000

while True:
    print('\t\tMENÚ CAJERO AUTOMÁTICO')
    print('=' * 40)
    print('1. Hacer depósito')
    print('2. Retirar dinero de la cuenta')
    print('3. Mostrar saldo disponible')
    print('4. Salir')
    print('=' * 40)
    
    opcion = int(input('Digite una opción del menú: '))
    
    if opcion == 1:
        deposito = float(input('Cantidad a ingresar: $'))
        if deposito > 0:
            saldo += deposito
            print(f'Tu nuevo saldo es de: ${saldo:.2f}')
        else:
            print('La cantidad a depositar debe ser mayor a 0')
    
    elif opcion == 2:
        retirar = float(input('Cuánto dinero deseas retirar: $'))
        if retirar > 0:
            if retirar <= saldo:
                saldo -= retirar
                print(f'Has retirado: ${retirar:.2f}')
                print(f'Tu nuevo saldo es: ${saldo:.2f}')
            else:
                print('No cuentas con saldo suficiente en tu cuenta')
                print(f'Saldo actual: ${saldo:.2f}')
        else:
            print('La cantidad a retirar debe ser mayor a 0')
    
    elif opcion == 3:
        print(f'Tu saldo disponible es de: ${saldo:.2f}')
    
    elif opcion == 4:
        print('Gracias por tu preferencia')
        print('¡Hasta luego!')
        break
    
    else:
        print('Por favor, seleccione una opción válida del menú (1-4)')
    
    print()  # Línea en blanco para mejor legibilidad
