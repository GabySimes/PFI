
 # Importamos la librería para trabajar con SQLite3 

import sqlite3 as sql 

# Función principal del programa
def main():  
    while True:
        print('''
          
     Elija una opción:

    1. Agregar Producto
    2. Mostrar Productos
    3. Actualizar Cantidad de Producto
    4. Eliminar Producto
    5. Buscar Producto
    6. Reporte de Bajo Stock
    7. Salir
        ''')
       
# Funcion principal, la funcion siempre vuelve a ejecutrase cada vez que se realice una accion valida en el programa        
        
        try:
            opcion = int(input('Elija una opción: '))
        except ValueError:
            print("Opción inválida. Debe ingresar un número entero.")
            continue  # Continuamos el bucle si no es un número válido

        if opcion == 1:
            print('Agregar Producto')
            registrar_producto()
        elif opcion == 2:
            print('Mostrar Productos')
            mostrar_productos()
        elif opcion == 3:
            print("Actualizar cantidad de producto")
            actualizar_cantidad()       
        elif opcion == 4:
            print("Eliminar producto")
            eliminar_producto()
        elif opcion == 5:
            print("Buscar producto")
            buscar_producto()
        elif opcion == 6:
            print("Reporte de bajo stock")
            bajo_stock()
        elif opcion == 7:
            print("Saliendo del sistema...")
            break  # Salir del bucle y terminar el programa
        else:
            print("Opción inválida. Por favor, ingrese una opción válida.")
            continue

#creacion de base de datos
def create_data_base(): 
    conexion = sql.connect('inventario.db')
    conexion.commit()
    conexion.close()
    
#creacion tabla productos
def db_crear_tabla_productos(): 
    conexion = sql.connect('inventario.db') 
    cursor = conexion.cursor()  
    cursor.execute(
            """ 
            CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            categoria TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
            )
            """
        )
    conexion.commit()
    conexion.close()

create_data_base()
db_crear_tabla_productos()


#funcion para detener pantalla y visualizar terminal

def espera():
    print("")
    input(f"Enter para continuar")    

# Funcion registrar_producto, agrega producto al inventario

def registrar_producto(): 
    repetir = True  

    while repetir:
        nombre = input('Ingrese el nombre del producto: ')
        nombre = nombre.title()
        descripcion = input('Ingrese la descrición del producto: ')
        descripcion = descripcion.title()
        categoria = input('Ingrese la categoria: ')
        categoria = categoria.title()
        cantidad = int(input('Ingrese la cantidad: '))
        precio = float(input('Ingrese precio: '))


        conexion = sql.connect('inventario.db')
        cursor = conexion.cursor()
        instruccion = f"INSERT INTO productos(nombre , descripcion, categoria, cantidad, precio) VALUES(?, ? , ?, ?, ? )"
        cursor.execute(instruccion,(nombre, descripcion, categoria, cantidad,  precio))

        print(f" Producto '{nombre}' , agregado con exito " )    
        conexion.commit()
        conexion.close()

        consulta = input(f"¿ Desea agregar otro producto? (s) ").lower()
        if consulta == "s":
            repetir = True
        else:
            break
       
    
# Muestra el inventario con todos los campos 

def mostrar_productos():
    conexion = sql.connect('inventario.db')
    cursor = conexion.cursor()
    instruccion = f" SELECT * FROM productos"
    cursor.execute(instruccion)
    mostrar = cursor.fetchall()
    conexion.commit()
    conexion.close()


    if not mostrar:
        # si la base de datos este vacia
        print('No hay productos en el inventario')
        espera ()
    else:
        print('Inventario actual: ')
   
        for i in mostrar:
            id, nombre, descripcion, categoria, cantidad, precio = i
            print(f'''ID: {id}
            Nombre: {nombre}
            Descripcion: {descripcion}
            Categoria: {categoria} 
            Cantidad: {cantidad}
            Precio: {precio}
                  
        ''')
        espera ()

# Funcion actualizar , actualiza la canditad del producto seleccionandolo por su ID 

def actualizar_cantidad():
    conexion = sql.connect('inventario.db')
    cursor = conexion.cursor()

    try:
        id_producto = int(input("Ingrese el ID del producto a actualizar: "))

        # Obtener el nombre del producto basado en el ID
        cursor.execute("SELECT nombre FROM productos WHERE id=?", (id_producto,))
        resultado = cursor.fetchone()

        if resultado:
            nombre_producto = resultado[0]
            print(f"El producto a actualizar es: {nombre_producto}")

            # Confirmación al usuario
            nueva_cantidad = int(input("Ingrese la nueva cantidad: "))

            # Actualizar la cantidad
            cursor.execute("UPDATE productos SET cantidad=? WHERE id=?", (nueva_cantidad, id_producto,))

            # Comprobar si se actualizaron filas
            filas_afectadas = cursor.rowcount
            if filas_afectadas > 0:
                print(f"Se actualizó la cantidad del producto {nombre_producto} a {nueva_cantidad} unidades")
                espera ()
            else:
                print(f"No se encontró ningún producto con ID {id_producto}")
                espera ()
        else:
            print(f"No se encontró ningún producto con ID {id_producto}")
            espera ()

    except ValueError:
        print("Error: Debe ingresar un ID válido (número entero)")
    except sql.Error as e:
        print(f"Error al actualizar la cantidad: {e}")
    finally:
        conexion.commit()
        conexion.close()


# Funcion eliminar_producto, elimina un producto seleccionandolo por su ID

def eliminar_producto():
    conexion = sql.connect('inventario.db')
    cursor = conexion.cursor()
    id_producto = input('Qué ID quieres eliminar? ')

    # Obtener información del producto a eliminar
    cursor.execute("SELECT nombre FROM productos WHERE id=?", (id_producto,))
    resultado = cursor.fetchone()

    # Verificar si se encontró el producto
    if resultado:
        nombre_producto = resultado[0]
        # Confirmación al usuario
        confirmar = input(f"¿Estás seguro de que deseas eliminar el producto '{nombre_producto}' con ID {id_producto}? (s/n): ")
        if confirmar.lower() != 's':
            print("Eliminación cancelada.")
            conexion.close()
            espera ()
            return

        # Eliminar el producto
        cursor.execute("DELETE FROM productos WHERE id=?", (id_producto,))
        conexion.commit()
        print(f"El producto '{nombre_producto}' con ID {id_producto} fue eliminado correctamente")
        espera ()
    else:
        print('No se encontró ningún producto con ese ID.')
        espera ()

    conexion.close()



# Funcion buscar_producto, busca un producto por nombre, categoria o ID

def buscar_producto():
    conexion = sql.connect('inventario.db')
    cursor = conexion.cursor()

    try:
        criterio = int(input("¿Por qué criterio desea buscar? (1-ID, 2-nombre, 3-categoría): "))
        valor_busqueda = input("Ingrese el valor a buscar: ")

        if criterio == 1:
            cursor.execute("SELECT * FROM productos WHERE id=?", (valor_busqueda,))
        elif criterio == 2:
            cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + valor_busqueda + '%',))
        elif criterio == 3:
            cursor.execute("SELECT * FROM productos WHERE categoria LIKE ?", ('%' + valor_busqueda + '%',))
        else:
            print("Criterio de búsqueda no válido.")
            return

        resultados = cursor.fetchall()
        if resultados:
            print("Resultados de la búsqueda:")
            for i in resultados:
                id, nombre, descripcion, categoria, cantidad, precio = i
                print(f'''ID: {id}
                Nombre: {nombre}
                Descripcion: {descripcion}
                Categoria: {categoria}  
                Cantidad: {cantidad}
                Precio: {precio}
                      
            ''')
            espera ()
        else:
            print("No se encontraron productos que coincidan con su búsqueda.")
            espera()

    except ValueError:
        print("El criterio de búsqueda debe ser un número entre 1 y 3.")

    finally:
        conexion.close()
    

# Funcion bajo_stock, muestra los productos que tienen stock por debajo de un umbral

def bajo_stock():
    conexion = sql.connect('inventario.db')
    cursor = conexion.cursor()
    umbral = int(input('Cual es el umbral de stock que quierer revisar ? '))
    cursor.execute("SELECT * FROM productos WHERE cantidad < ?", (umbral,))
    productos_bajo_stock  = cursor.fetchall()

    if not productos_bajo_stock:
        print(f"No hay productos con stock por debajo de {umbral}.")
        espera ()
    else:
        print(f"Productos con stock por debajo de {umbral}:")
        for producto in productos_bajo_stock:
            id, nombre, descripcion, categoria, cantidad, precio = producto
            print(f'''ID: {id}
            Nombre: {nombre}
            Descripcion: {descripcion}
            Categoria: {categoria} 
            Cantidad: {cantidad}
            Precio: {precio}
                  
        ''')
            
        espera ()    
    conexion.close()    
       
# Ejecución de la función main()
if __name__ == "__main__":
    main()
