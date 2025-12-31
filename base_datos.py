import mysql.connector
from mysql.connector import Error
import sys
from datetime import datetime

class GestionInventario:
    def __init__(self, host='localhost', database='gestion_inventario', 
                 user='root', password=''):
        """
        Inicializa la conexión a la base de datos
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        
    def conectar(self):
        """
        Establece conexión con la base de datos
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print("✅ Conexión exitosa a la base de datos")
                return True
                
        except Error as e:
            print(f"❌ Error al conectar a MySQL: {e}")
            return False
    
    def desconectar(self):
        """
        Cierra la conexión a la base de datos
        """
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("🔌 Conexión cerrada")
    
    # ========== OPERACIONES CRUD PARA CATEGORÍAS ==========
    
    def crear_categoria(self, nombre, descripcion=""):
        """
        Crea una nueva categoría
        """
        try:
            query = """
            INSERT INTO categorias (nombre_categoria, descripcion)
            VALUES (%s, %s)
            """
            valores = (nombre, descripcion)
            
            self.cursor.execute(query, valores)
            self.connection.commit()
            print(f"✅ Categoría '{nombre}' creada exitosamente")
            return self.cursor.lastrowid
            
        except Error as e:
            print(f"❌ Error al crear categoría: {e}")
            return None
    
    def listar_categorias(self):
        """
        Lista todas las categorías
        """
        try:
            query = "SELECT * FROM categorias ORDER BY nombre_categoria"
            self.cursor.execute(query)
            categorias = self.cursor.fetchall()
            
            if categorias:
                print("\n" + "="*60)
                print("📂 LISTA DE CATEGORÍAS")
                print("="*60)
                for cat in categorias:
                    print(f"ID: {cat['id_categoria']}")
                    print(f"Nombre: {cat['nombre_categoria']}")
                    print(f"Descripción: {cat['descripcion'][:50] if cat['descripcion'] else 'Sin descripción'}")
                    print(f"Creada: {cat['fecha_creacion']}")
                    print("-"*40)
            else:
                print("ℹ️ No hay categorías registradas")
                
            return categorias
            
        except Error as e:
            print(f"❌ Error al listar categorías: {e}")
            return []
    
    # ========== OPERACIONES CRUD PARA PRODUCTOS ==========
    
    def crear_producto(self, codigo_barras, nombre, id_categoria, precio, cantidad=0):
        """
        Crea un nuevo producto
        """
        try:
            query = """
            INSERT INTO productos (codigo_barras, nombre_producto, id_categoria, precio, cantidad)
            VALUES (%s, %s, %s, %s, %s)
            """
            valores = (codigo_barras, nombre, id_categoria, precio, cantidad)
            
            self.cursor.execute(query, valores)
            self.connection.commit()
            print(f"✅ Producto '{nombre}' creado exitosamente")
            return self.cursor.lastrowid
            
        except Error as e:
            print(f"❌ Error al crear producto: {e}")
            return None
    
    def buscar_producto(self, criterio, valor):
        """
        Busca productos por diferentes criterios
        """
        try:
            if criterio == "codigo":
                query = """
                SELECT p.*, c.nombre_categoria 
                FROM productos p 
                JOIN categorias c ON p.id_categoria = c.id_categoria 
                WHERE p.codigo_barras = %s
                """
            elif criterio == "nombre":
                query = """
                SELECT p.*, c.nombre_categoria 
                FROM productos p 
                JOIN categorias c ON p.id_categoria = c.id_categoria 
                WHERE p.nombre_producto LIKE %s
                """
                valor = f"%{valor}%"
            elif criterio == "categoria":
                query = """
                SELECT p.*, c.nombre_categoria 
                FROM productos p 
                JOIN categorias c ON p.id_categoria = c.id_categoria 
                WHERE c.nombre_categoria = %s
                """
            else:
                print("❌ Criterio de búsqueda no válido")
                return []
            
            self.cursor.execute(query, (valor,))
            productos = self.cursor.fetchall()
            
            if productos:
                print(f"\n🔍 Resultados de búsqueda ({len(productos)} encontrados):")
                self._mostrar_productos(productos)
            else:
                print("ℹ️ No se encontraron productos con ese criterio")
                
            return productos
            
        except Error as e:
            print(f"❌ Error en búsqueda: {e}")
            return []
    
    def listar_productos(self, ordenar_por="nombre"):
        """
        Lista todos los productos con opción de ordenamiento
        """
        try:
            orden = {
                "nombre": "p.nombre_producto",
                "categoria": "c.nombre_categoria",
                "precio": "p.precio DESC",
                "cantidad": "p.cantidad DESC"
            }.get(ordenar_por, "p.nombre_producto")
            
            query = f"""
            SELECT p.*, c.nombre_categoria 
            FROM productos p 
            JOIN categorias c ON p.id_categoria = c.id_categoria 
            ORDER BY {orden}
            """
            
            self.cursor.execute(query)
            productos = self.cursor.fetchall()
            
            if productos:
                print(f"\n📦 LISTA DE PRODUCTOS (Ordenados por: {ordenar_por})")
                print("="*80)
                self._mostrar_productos(productos)
            else:
                print("ℹ️ No hay productos registrados")
                
            return productos
            
        except Error as e:
            print(f"❌ Error al listar productos: {e}")
            return []
    
    def actualizar_producto(self, codigo_barras, campo, nuevo_valor):
        """
        Actualiza información de un producto
        """
        try:
            campos_permitidos = ['nombre_producto', 'id_categoria', 'precio', 'cantidad']
            
            if campo not in campos_permitidos:
                print(f"❌ Campo '{campo}' no es válido para actualizar")
                return False
            
            query = f"UPDATE productos SET {campo} = %s WHERE codigo_barras = %s"
            valores = (nuevo_valor, codigo_barras)
            
            self.cursor.execute(query, valores)
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                print(f"✅ Producto actualizado exitosamente")
                return True
            else:
                print("ℹ️ No se encontró el producto con ese código de barras")
                return False
                
        except Error as e:
            print(f"❌ Error al actualizar producto: {e}")
            return False
    
    def eliminar_producto(self, codigo_barras):
        """
        Elimina un producto por código de barras
        """
        try:
            # Primero verificar si existe
            self.cursor.execute("SELECT nombre_producto FROM productos WHERE codigo_barras = %s", (codigo_barras,))
            producto = self.cursor.fetchone()
            
            if not producto:
                print("❌ No se encontró el producto")
                return False
            
            confirmacion = input(f"¿Estás seguro de eliminar '{producto['nombre_producto']}'? (s/n): ")
            
            if confirmacion.lower() == 's':
                query = "DELETE FROM productos WHERE codigo_barras = %s"
                self.cursor.execute(query, (codigo_barras,))
                self.connection.commit()
                
                if self.cursor.rowcount > 0:
                    print("✅ Producto eliminado exitosamente")
                    return True
                else:
                    print("❌ Error al eliminar el producto")
                    return False
            else:
                print("❌ Eliminación cancelada")
                return False
                
        except Error as e:
            print(f"❌ Error al eliminar producto: {e}")
            return False
    
    def actualizar_inventario(self, codigo_barras, cantidad, operacion='agregar'):
        """
        Actualiza la cantidad en inventario
        operacion: 'agregar', 'restar' o 'establecer'
        """
        try:
            if operacion == 'agregar':
                query = "UPDATE productos SET cantidad = cantidad + %s WHERE codigo_barras = %s"
            elif operacion == 'restar':
                query = "UPDATE productos SET cantidad = cantidad - %s WHERE codigo_barras = %s"
            elif operacion == 'establecer':
                query = "UPDATE productos SET cantidad = %s WHERE codigo_barras = %s"
            else:
                print("❌ Operación no válida")
                return False
            
            self.cursor.execute(query, (cantidad, codigo_barras))
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                print(f"✅ Inventario actualizado exitosamente")
                return True
            else:
                print("❌ No se encontró el producto")
                return False
                
        except Error as e:
            print(f"❌ Error al actualizar inventario: {e}")
            return False
    
    # ========== REPORTES Y CONSULTAS ESPECIALES ==========
    
    def reporte_inventario_bajo(self, limite=10):
        """
        Muestra productos con inventario bajo
        """
        try:
            query = """
            SELECT p.*, c.nombre_categoria 
            FROM productos p 
            JOIN categorias c ON p.id_categoria = c.id_categoria 
            WHERE p.cantidad < %s 
            ORDER BY p.cantidad ASC
            """
            
            self.cursor.execute(query, (limite,))
            productos = self.cursor.fetchall()
            
            if productos:
                print(f"\n⚠️ PRODUCTOS CON INVENTARIO BAJO (menos de {limite} unidades)")
                print("="*80)
                self._mostrar_productos(productos)
            else:
                print(f"✅ Todos los productos tienen más de {limite} unidades")
                
            return productos
            
        except Error as e:
            print(f"❌ Error al generar reporte: {e}")
            return []
    
    def valor_total_inventario(self):
        """
        Calcula el valor total del inventario
        """
        try:
            query = "SELECT SUM(precio * cantidad) as total FROM productos"
            self.cursor.execute(query)
            resultado = self.cursor.fetchone()
            
            total = resultado['total'] if resultado['total'] else 0
            print(f"\n💰 VALOR TOTAL DEL INVENTARIO: ${total:,.2f}")
            return total
            
        except Error as e:
            print(f"❌ Error al calcular valor total: {e}")
            return 0
    
    # ========== MÉTODOS AUXILIARES ==========
    
    def _mostrar_productos(self, productos):
        """
        Muestra productos en formato tabular
        """
        print(f"{'Código Barras':<15} {'Nombre':<25} {'Categoría':<15} {'Precio':<10} {'Cantidad':<10}")
        print("-"*80)
        
        for prod in productos:
            print(f"{prod['codigo_barras'][:15]:<15} "
                  f"{prod['nombre_producto'][:23]:<25} "
                  f"{prod['nombre_categoria'][:13]:<15} "
                  f"${prod['precio']:<9.2f} "
                  f"{prod['cantidad']:<10}")
    
    def obtener_categoria_id(self, nombre_categoria):
        """
        Obtiene el ID de una categoría por nombre
        """
        try:
            query = "SELECT id_categoria FROM categorias WHERE nombre_categoria = %s"
            self.cursor.execute(query, (nombre_categoria,))
            resultado = self.cursor.fetchone()
            
            if resultado:
                return resultado['id_categoria']
            else:
                print(f"❌ Categoría '{nombre_categoria}' no encontrada")
                return None
                
        except Error as e:
            print(f"❌ Error al buscar categoría: {e}")
            return None


# ========== INTERFAZ DE USUARIO ==========

def mostrar_menu():
    """
    Muestra el menú principal
    """
    print("\n" + "="*50)
    print("🏪 SISTEMA DE GESTIÓN DE INVENTARIO")
    print("="*50)
    print("1. 📦 Listar productos")
    print("2. 🔍 Buscar producto")
    print("3. ➕ Crear nuevo producto")
    print("4. ✏️ Actualizar producto")
    print("5. 🗑️ Eliminar producto")
    print("6. 📊 Gestión de inventario")
    print("7. 📂 Gestionar categorías")
    print("8. 📈 Reportes")
    print("9. ℹ️ Ver información del sistema")
    print("0. 🚪 Salir")
    print("="*50)

def main():
    """
    Función principal del programa
    """
    # Configuración de conexión (ajusta según tu entorno)
    gestor = GestionInventario(
        host='localhost',
        database='gestion_inventario',
        user='root',  # Cambia por tu usuario
        password=''   # Cambia por tu contraseña
    )
    
    # Intentar conectar
    if not gestor.conectar():
        print("No se pudo conectar a la base de datos. Verifica la configuración.")
        return
    
    while True:
        mostrar_menu()
        opcion = input("\n👉 Selecciona una opción: ")
        
        if opcion == "1":  # Listar productos
            print("\nOpciones de ordenamiento:")
            print("1. Por nombre")
            print("2. Por categoría")
            print("3. Por precio (mayor a menor)")
            print("4. Por cantidad (mayor a menor)")
            
            orden_opcion = input("Selecciona orden (1-4, default=1): ")
            orden_map = {"1": "nombre", "2": "categoria", "3": "precio", "4": "cantidad"}
            orden = orden_map.get(orden_opcion, "nombre")
            
            gestor.listar_productos(orden)
            
        elif opcion == "2":  # Buscar producto
            print("\nCriterios de búsqueda:")
            print("1. Por código de barras")
            print("2. Por nombre")
            print("3. Por categoría")
            
            criterio_opcion = input("Selecciona criterio (1-3): ")
            criterio_map = {"1": "codigo", "2": "nombre", "3": "categoria"}
            criterio = criterio_map.get(criterio_opcion, "nombre")
            
            valor = input("Ingresa el valor a buscar: ")
            gestor.buscar_producto(criterio, valor)
            
        elif opcion == "3":  # Crear producto
            print("\n📝 CREAR NUEVO PRODUCTO")
            
            # Mostrar categorías disponibles
            gestor.listar_categorias()
            
            codigo = input("Código de barras: ")
            nombre = input("Nombre del producto: ")
            categoria_nombre = input("Nombre de la categoría: ")
            precio = float(input("Precio: "))
            cantidad = int(input("Cantidad inicial: "))
            
            # Obtener ID de categoría
            categoria_id = gestor.obtener_categoria_id(categoria_nombre)
            
            if categoria_id:
                gestor.crear_producto(codigo, nombre, categoria_id, precio, cantidad)
            else:
                print("❌ No se puede crear el producto sin categoría válida")
            
        elif opcion == "4":  # Actualizar producto
            print("\n✏️ ACTUALIZAR PRODUCTO")
            codigo = input("Código de barras del producto a actualizar: ")
            
            print("\nCampos disponibles para actualizar:")
            print("1. Nombre")
            print("2. Categoría")
            print("3. Precio")
            print("4. Cantidad")
            
            campo_opcion = input("Selecciona campo (1-4): ")
            campo_map = {"1": "nombre_producto", "2": "id_categoria", 
                        "3": "precio", "4": "cantidad"}
            campo = campo_map.get(campo_opcion)
            
            if campo:
                if campo == "id_categoria":
                    gestor.listar_categorias()
                    nuevo_valor = int(input("Nuevo ID de categoría: "))
                elif campo == "precio":
                    nuevo_valor = float(input("Nuevo precio: "))
                elif campo == "cantidad":
                    nuevo_valor = int(input("Nueva cantidad: "))
                else:
                    nuevo_valor = input("Nuevo valor: ")
                
                gestor.actualizar_producto(codigo, campo, nuevo_valor)
            else:
                print("❌ Opción no válida")
            
        elif opcion == "5":  # Eliminar producto
            print("\n🗑️ ELIMINAR PRODUCTO")
            codigo = input("Código de barras del producto a eliminar: ")
            gestor.eliminar_producto(codigo)
            
        elif opcion == "6":  # Gestión de inventario
            print("\n📊 GESTIÓN DE INVENTARIO")
            codigo = input("Código de barras del producto: ")
            
            print("\nOperaciones disponibles:")
            print("1. Agregar unidades")
            print("2. Restar unidades")
            print("3. Establecer cantidad")
            
            operacion_opcion = input("Selecciona operación (1-3): ")
            operacion_map = {"1": "agregar", "2": "restar", "3": "establecer"}
            operacion = operacion_map.get(operacion_opcion)
            
            if operacion:
                cantidad = int(input("Cantidad: "))
                gestor.actualizar_inventario(codigo, cantidad, operacion)
            else:
                print("❌ Operación no válida")
            
        elif opcion == "7":  # Gestionar categorías
            print("\n📂 GESTIÓN DE CATEGORÍAS")
            print("1. Listar categorías")
            print("2. Crear nueva categoría")
            
            cat_opcion = input("Selecciona opción (1-2): ")
            
            if cat_opcion == "1":
                gestor.listar_categorias()
            elif cat_opcion == "2":
                nombre = input("Nombre de la nueva categoría: ")
                descripcion = input("Descripción (opcional): ")
                gestor.crear_categoria(nombre, descripcion)
            
        elif opcion == "8":  # Reportes
            print("\n📈 REPORTES")
            print("1. Productos con inventario bajo")
            print("2. Valor total del inventario")
            
            reporte_opcion = input("Selecciona reporte (1-2): ")
            
            if reporte_opcion == "1":
                limite = int(input("Límite de inventario bajo (default=10): ") or "10")
                gestor.reporte_inventario_bajo(limite)
            elif reporte_opcion == "2":
                gestor.valor_total_inventario()
            
        elif opcion == "9":  # Información del sistema
            print("\nℹ️ INFORMACIÓN DEL SISTEMA")
            print(f"Base de datos: {gestor.database}")
            print(f"Host: {gestor.host}")
            print(f"Usuario: {gestor.user}")
            print(f"Hora actual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Contar productos y categorías
            gestor.cursor.execute("SELECT COUNT(*) as total FROM productos")
            total_productos = gestor.cursor.fetchone()['total']
            
            gestor.cursor.execute("SELECT COUNT(*) as total FROM categorias")
            total_categorias = gestor.cursor.fetchone()['total']
            
            print(f"Total productos: {total_productos}")
            print(f"Total categorías: {total_categorias}")
            
        elif opcion == "0":  # Salir
            print("👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción no válida. Intenta de nuevo.")
        
        input("\nPresiona Enter para continuar...")
    
    # Desconectar al finalizar
    gestor.desconectar()

if __name__ == "__main__":
    # Instalación de dependencias necesarias
    try:
        import mysql.connector
    except ImportError:
        print("❌ mysql-connector-python no está instalado.")
        print("📦 Instálalo con: pip install mysql-connector-python")
        sys.exit(1)
    
    main()