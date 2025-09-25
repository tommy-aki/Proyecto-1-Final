Este gestor de base de datos MySQL es el proyecto de Tommy Lee Pon para Unitec. Está diseñado para ver, editar, crear, formar DDL, usar y ejecutar comandos SQL. Tiene la capacidad de configurar diferentes  conexiones MySQL, bases de datos, configurar tablas y demás. A continuación, dejo los pasos más importantes y las limitaciones del mismo.

# TECNOLOGÍAS
- Python: Lenguaje de programación en la que se hizo todo el proyecto. 
- Tkiner: Librería de interfaz visual de python. 
- MySQL_Connector: Librería de conexión de base de datos MySQL de Python. 

# ESTRUCTURA
Proyecto_Final
    /db
        connection.py
        querries.py
    /ventanas
        conexion_window.py
        edit_con_window.py
        main_window.py
    main.py
    README.md

# CARACTERÍSTICAS
- Conéxion a multiples bases de datos MySQL
- Creación de objetos con interfaz visual
- Ejecución de consultas SQL
- Creación y exportación de DDL
- Ver los objetos de la base de datos

# USO

## Para agregar una conexión:
1.  En la barra de Menu, dar click en "Conexión"
2.  En el submenu, dar click a Crear conexión. Abrirá una nueva ventana.
3.  Llenar con los datos requeridos y dar click en el botón Conectar. Un mensaje de confirmación aparecerá y será dirigido a la ventana principal

**LIMITACIÓN AL CONECTAR:**
La implementación solamente funciona si se especifica la Base de Datos. No hay disponibilidad para manejar multiples bases de datos en el mismo nodo. Esto debido a como se realizó el proyecto, ya que no guarda cual base de datos se está trabajando mediante el Querry "USE {db}". Todos los querries son realizados con un archivo db/querries.py, que cierra automáricamente el cursor despues de realizar sentencias.


## Para editar la conexión:
1.  Seleccionár la conexión con un click izquierdo.
2.  En la barra de menu, dar click en "Conexión"
3.  En el submenu, estará habilitada la opción "Editar Conexión". Dar click para abrir la ventana.
4.  Editar los datos de la nueva vetnna y dar click en el botón Conectar. Un mensaje de confirmación y será dirigído a la ventana principal.


## Para borrar la conexión:
1.  Seleccionár la conexión con un click izquierdo.
2.  En la barra de menu, dar click en "Conexión"
3.  En el submenu, estará habilitada la opción "Borrar Conexión". Dar click para abrir la ventana.
4.  Aparecerá un mensaje de confirmación de borrado. Dar clic en confirmar. Será dirigído a la ventana principal, y la conexión no se verá disponible.


## Para ver los objetos de la conexión:
1.  Realizar una conexión.
2.  Dar clic al botón (+) al lado del nombre de la conexión. Este expandirá el nodo mostrando las tablas, vistas, indices, procedimientos, funciones, y disparadores
3.  Para ver los componentes, dar clic al botón (+) al lado del tipo de objeto. Este expandirá el nodo mostrando el nombre de los objetos especificados. 

**LIMITACIÓN:**
Hubo 3 objetos que no se pudieron incluir:
1.  MySQL no maneja secuencias ni paquetes. Por ende, no hay comando para mostrarlos.
2.  MySQL no tiene forma de mostrar los usuarios mediante comandos SHOW. MySQL  obtiene sus usuarios mediante Information Schema.
3.  Debido a la decisión técnia del principio, mi gestor no muestra las bases de datos o tablespaces, pues se define al momento de crear o editar la conexión.
 

## Para ver el DDL de los objetos:
1.  Abrir completamente los nodos.
2.  Sobre el nodo el cual desea ver el DDL, dar click derecho.
3.  En el submenu, dar click en "Ver DDL"
4.  En el notebook, en la sección de comando, se escribirá el "CREATE DDL" para el objeto seleccionado.


## Para realizar comandos con SQL
1.  Escoger la rama de nodos de donde quiere ejecutar el querry.
2.  En la ventana grande, debajo de donde dice "Consola SQL:", escribir la sentencia SQL deseada.
3.  Al terminar la sentencia, dar clic en el botón "EJECUTAR"
4.  Arriba de esa ventana, se mostrará el resultado. Si la sentencia fue un SELECT, mostrará la tabla de resultado. Si fue un UPDATE, DELETE, o CREATE, un mensaje de confirmación de la sentencia se verá reflejado indicando el número de filas alteradas


-----------------------------------------------------------------------------------------------------------
# Parte 2

# Tecnologías
- Psycopg2: Librería de Python para conectar con bases de datos PostgreSQL.
- Mermaid/IPython: Librería para crear diagramas de entidad-relación usado para generar el diagrama.
- PyWebView: Librería de python para crear views con HTML con soporte para Scripts

# ESTRUCTURA
Proyecto_Final
    /db
        connection.py
        querries.py
        erd.py                  // encargada de generar los diccionarios para el diagrama
        export.py               // encargada de syncronizar los datos
    /Graphviz                   // ejecutable de graphviz (Inutilizado)
    /ventanas
        conexion_window.py
        edit_con_window.py
        erd_window.py           // ventana que crea y muestra el diagrama ER
        sync_window.py          // ventana que pide los datos de conexión PostgreSQL
        main_window.py
    main.py
    README.md

# CARACTERÍSTICAS
- Sincronización con base de datos PostgreSQL
- Crear diagrama de Entidad Relación

# USO

## Para crear sincronizar con bases de datos PostgreSQL
1.  Con una conexión seleccionada, click en Conexión
2.  En el submenu, dar click a "Exportar a PostgreSQL". Abrirá una nueva ventana.
3.  Llenar con los datos requeridos y dar click en el botón Conectar. Un mensaje de confirmación aparecerá y será dirigido a la ventana principal, con la base de datos ya sincronizada

## Para ver el diagrama ERD
1.  Abrir una conexión y  click derecho sobre una tabla
2.  En el submenu, seleccionar la opción "Ver ERD"
3.  Abrirá una ventana nueva en la que podrá ver el diagrama con la tablas, llaves foráneas y columnas