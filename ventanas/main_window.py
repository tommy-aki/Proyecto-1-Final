import tkinter as tk
from tkinter import N, S, W, E
from tkinter import ttk, messagebox
from ventanas.conexion_window import conexion_window
from ventanas.edit_con_window import  edit_window
from db.connection import ConnectionManager as cm
from db.querries import query
from db.export import export

def main_window():
    conn_manager = cm()


    def add_connection_to_ui(nombre, db):
        node = tree.insert("", "end", iid=nombre, text=nombre)
        print(f"Conexión agregada: {nombre}")

        connection = conn_manager.get_conexion(nombre)
        cursor = connection.cursor()
        cursor.execute(f"USE {db};")

        tab = tree.insert(node, "end", iid=f"{nombre}_tab", text="Tablas")
        cursor.execute("SHOW FULL TABLES WHERE Table_type='BASE TABLE';")
        tables  = cursor.fetchall()
        if tables:
            for(table, type_) in tables:
                tree.insert(tab, "end", iid=f"{nombre}_tab_{table}", text=table)

        vi = tree.insert(node, "end", iid=f"{nombre}_vis", text="Vistas")
        cursor.execute("SHOW FULL TABLES WHERE Table_type='VIEW';")
        views = cursor.fetchall()
        if views:
            for(view, type_) in views:
                tree.insert(vi, "end", iid=f"{nombre}_vis_{view}", text=view)

        ind = tree.insert(node, "end", iid=f"{nombre}_ind", text="Indices")
        for(table, type_) in tables:
            cursor.execute(f"SHOW INDEX FROM {table};")
            indexes = cursor.fetchall()
            if indexes:
                for index in indexes:
                    tree.insert(ind, "end", iid=f"{nombre}_ind_{index[0]}.{index[2]}.{index[4]}", text=f"{index[0]}.{index[2]}.{index[4]}")

        proc = tree.insert(node, "end", iid=f"{nombre}_proc", text="Procedimientos")
        cursor.execute(f"SHOW PROCEDURE STATUS WHERE Db='{db}';")
        procedures = cursor.fetchall()
        if procedures:
            for procedure in procedures:
                tree.insert(proc, "end", iid=f"{nombre}_proc_{procedure[1]}", text=procedure[1])

        func = tree.insert(node, "end", iid=f"{nombre}_func", text="Funciones")
        cursor.execute(f"SHOW FUNCTION STATUS WHERE Db='{db}';")
        functions = cursor.fetchall()
        if functions:
            for function in functions:
                tree.insert(func, "end", iid=f"{nombre}_func_{function[1]}", text=function[1])

        trig = tree.insert(node, "end", iid=f"{nombre}_trig", text="Triggers")
        cursor.execute(f"SHOW TRIGGERS FROM {db};")
        triggers = cursor.fetchall()
        if triggers:
            for trigger in triggers:
                tree.insert(trig, "end", iid=f"{nombre}_trig_{trigger[0]}", text=trigger[0])
        cursor.close()

    def add_connection():
        conexion_window(root, conn_manager, add_connection_to_ui)
    
    def on_double_click(event):
        item_id = tree.focus()
        if not item_id:
            return

        if "_tab_" in item_id:
            nombre, tabla = item_id.split("_tab_", 1)
            col, rows = query(conn_manager.get_conexion(nombre), f"SHOW TABLE STATUS WHERE Name = '{tabla}'")      
            new_tab = ttk.Frame(notebook)
            notebook.add(new_tab, text=tabla)
            notebook.select(new_tab)

            ttk.Label(new_tab, text="Nombre:", padding="5 0 0 0").grid(column=0, row=0, sticky=E)
            name = ttk.Entry(new_tab, width=32)
            name.insert(0, rows[0]['Name'])
            name.grid(column=1, row=0, sticky=W, pady=7)
            
            ttk.Label(new_tab, text="Motor:", padding="5 0 0 0").grid(column=0, row=1, sticky=E)
            motor = ttk.Entry(new_tab, width=32)
            motor.insert(0, rows[0]['Engine'])
            motor.grid(column=1, row=1, sticky=W, pady=7)

            cols, rows = query(conn_manager.get_conexion(nombre), f"SHOW COLUMNS FROM `{tabla}`")

            columns = ttk.Treeview(new_tab, columns=cols, show="headings", padding="5 0 0 0")
            columns.grid(column=1, row=2)

            for col in cols:
                columns.heading(col, text=col)
                columns.column(col, width=120, anchor="w")
                if col in ('Null', 'Key', 'Default', 'Extra'):
                    columns.column(col, width=60)

            for row in rows:
                values = [row[col] for col in cols]
                columns.insert("", "end", values=values)

            view_button = ttk.Button(new_tab,  text="Ver Datos", command=lambda: ver_datos(tabla, nombre))
            view_button.grid(column=2, row=2, sticky=E)

            close_button = ttk.Button(new_tab,  text="Cerrar Ventana", command=lambda: notebook.forget(new_tab))
            close_button.grid(column=3, row=2, sticky=E)

        elif "_vis_" in item_id:
            nombre, view = item_id.split("_vis_", 1)
            col, rows = query(conn_manager.get_conexion(nombre), f"SHOW CREATE VIEW `{view}`")
            
            new_tab = ttk.Frame(notebook)
            notebook.add(new_tab, text=view)
            notebook.select(new_tab)

            ttk.Label(new_tab, text="Nombre:", padding="5 0 0 0").grid(column=0, row=0, sticky=E)
            name = ttk.Entry(new_tab, width=32)
            name.insert(0, view)
            name.grid(column=1, row=0, sticky=W, pady=7)

            ttk.Label(new_tab, text="Definición:", padding="5 0 0 0").grid(column=0, row=1, sticky=(N, E))
            definition = tk.Text(new_tab, width=60, height=10)
            definition.insert("1.0", rows[0]['Create View'])
            definition.grid(column=1, row=1, sticky=W, pady=7)

            cols, rows = query(conn_manager.get_conexion(nombre), f"SHOW COLUMNS FROM `{view}`")
            columns = ttk.Treeview(new_tab, columns=cols, show="headings", padding="5 0 0 0")
            columns.grid(column=1, row=2, sticky="nsew")

            for col in cols:
                columns.heading(col, text=col)
                columns.column(col, width=120, anchor="w")
                if col in ('Null', 'Key', 'Default', 'Extra'):
                    columns.column(col, width=60)

            for row in rows:
                values = [row[col] for col in cols]
                columns.insert("", "end", values=values)

            view_button = ttk.Button(new_tab, text="Ver Datos", command=lambda: ver_datos(view, nombre))
            view_button.grid(column=2, row=2, sticky=E, padx=5)

            close_button = ttk.Button(new_tab, text="Cerrar Ventana", command=lambda: notebook.forget(new_tab))
            close_button.grid(column=3, row=2, sticky=E, padx=5)

        elif "_ind_" in item_id:
            nombre, indice = item_id.split("_ind_", 1)
            idtab, idname, idcol = indice.split('.', 2)
            col, rows = query(conn_manager.get_conexion(nombre),f"SHOW INDEX FROM `{idtab}` WHERE Key_name = '{idname}'")
            new_tab = ttk.Frame(notebook)
            notebook.add(new_tab, text=indice)
            notebook.select(new_tab)

            ttk.Label(new_tab, text="Tabla:", padding="5 0 0 0").grid(column=0, row=0, sticky=E)
            tabla_entry = ttk.Entry(new_tab, width=32)
            tabla_entry.insert(0, idtab)
            tabla_entry.grid(column=1, row=0, sticky=W, pady=7)

            ttk.Label(new_tab, text="Nombre índice:", padding="5 0 0 0").grid(column=0, row=1, sticky=E)
            name_entry = ttk.Entry(new_tab, width=32)
            name_entry.insert(0, idname)
            name_entry.grid(column=1, row=1, sticky=W, pady=7)

            cols = ["Seq_in_index", "Column_name", "Collation", "Cardinality", "Sub_part", "Packed", "Null", "Index_type"]
            columns = ttk.Treeview(new_tab, columns=cols, show="headings", padding="5 0 0 0", height=6)
            columns.grid(column=0, row=2, columnspan=2, sticky="nsew")

            for col_name in cols:
                columns.heading(col_name, text=col_name)
                columns.column(col_name, width=100, anchor="w")

            for row in rows:
                values = [row.get(c, "") if isinstance(row, dict) else row[i] for i, c in enumerate(cols)]
                columns.insert("", "end", values=values)

            close_button = ttk.Button(new_tab, text="Cerrar Ventana", command=lambda: notebook.forget(new_tab))
            close_button.grid(column=1, row=3, sticky=E, pady=7)




        elif "_proc_" in item_id:
            nombre, proc = item_id.split("_proc_", 1)
            col, rows = query(conn_manager.get_conexion(nombre), f"SHOW PROCEDURE STATUS WHERE Name = '{proc}'") 
            new_tab = ttk.Frame(notebook)
            notebook.add(new_tab, text=proc)
            notebook.select(new_tab)

            ttk.Label(new_tab, text="Nombre:", padding="5 0 0 0").grid(column=0, row=0, sticky=E)
            name = ttk.Entry(new_tab, width=32)
            name.insert(0, rows[0]['Name'])
            name.grid(column=1, row=0, sticky=W, pady=7)

            ttk.Label(new_tab, text="Type:", padding="5 0 0 0").grid(column=0, row=1, sticky=E)
            type = ttk.Entry(new_tab, width=32)
            type.insert(0, rows[0]['Type'])
            type.grid(column=1, row=1, sticky=W, pady=7)

            ttk.Label(new_tab, text="Language:", padding="5 0 0 0").grid(column=0, row=2, sticky=E)
            res = ttk.Entry(new_tab, width=32)
            res.insert(0, rows[0]['Language'])
            res.grid(column=1, row=2, sticky=W, pady=7)

        elif "_func_" in item_id:
            nombre, proc = item_id.split("_func_", 1)
            col, rows = query(conn_manager.get_conexion(nombre), f"SHOW FUNCTION STATUS WHERE Name = '{proc}'") 
            new_tab = ttk.Frame(notebook)
            notebook.add(new_tab, text=proc)
            notebook.select(new_tab)

            ttk.Label(new_tab, text="Nombre:", padding="5 0 0 0").grid(column=0, row=0, sticky=E)
            name = ttk.Entry(new_tab, width=32)
            name.insert(0, rows[0]['Name'])
            name.grid(column=1, row=0, sticky=W, pady=7)

            ttk.Label(new_tab, text="Type:", padding="5 0 0 0").grid(column=0, row=1, sticky=E)
            type = ttk.Entry(new_tab, width=32)
            type.insert(0, rows[0]['Type'])
            type.grid(column=1, row=1, sticky=W, pady=7)

            ttk.Label(new_tab, text="Language:", padding="5 0 0 0").grid(column=0, row=2, sticky=E)
            res = ttk.Entry(new_tab, width=32)
            res.insert(0, rows[0]['Language'])
            res.grid(column=1, row=2, sticky=W, pady=7)

        elif "_trig_" in item_id:
            nombre, trig = item_id.split("_trig_", 1)
            host, db = nombre.split("/", 1)
            col, rows = query(conn_manager.get_conexion(nombre), f"SHOW triggers FROM {db} where `Trigger` = '{trig}';") 
            new_tab = ttk.Frame(notebook)
            notebook.add(new_tab, text=trig)
            notebook.select(new_tab)

            ttk.Label(new_tab, text="Nombre:", padding="5 0 0 0").grid(column=0, row=0, sticky=E)
            name = ttk.Entry(new_tab, width=32)
            name.insert(0, rows[0]['Trigger'])
            name.grid(column=1, row=0, sticky=W, pady=7)

            ttk.Label(new_tab, text="Tiempo:", padding="5 0 0 0").grid(column=0, row=1, sticky=E)
            Tiempo = ttk.Entry(new_tab, width=32)
            Tiempo.insert(0, rows[0]['Timing'])
            Tiempo.grid(column=1, row=1, sticky=W, pady=7)

            ttk.Label(new_tab, text="Evento:", padding="5 0 0 0").grid(column=0, row=2, sticky=E)
            ev = ttk.Entry(new_tab, width=32)
            ev.insert(0, rows[0]['Event'])
            ev.grid(column=1, row=2, sticky=W, pady=7)

    def edit_connection_in_ui(nombre, db):
        if nombre not in tree.get_children(""):
            add_connection_to_ui(nombre, db)
            del_connection()

    def edit_connection():
        selected = tree.selection()
        if selected:
            edit_window(root, conn_manager, selected[0], edit_connection_in_ui)
    
    def del_connection():
        selected = tree.selection()
        if selected:
            confirm = messagebox.askyesno("Confirmar", f"¿Borrar conexión {selected[0]}?")
            if confirm:
                #conn_manager.cerrar_conexion(selected[0])
                tree.delete(selected[0])
        tree.selection_clear()
        command.config(state="disabled")
        return

    def exp_connection():
        selected = tree.selection()

            
        if selected:
            confirm = messagebox.askyesno("Confirmar", f"¿Desea exportar {selected[0]} a PostgreSQL?")
            if confirm:
                export(conn_manager.get_conexion(selected[0]))

    def ejecutar_en_conexion():
        for item in result.get_children():
            result.delete(item)

        seleccion = tree.focus()
        parent = tree.parent(seleccion)
        if parent != "":
            while parent != "":
                seleccion = parent
                parent = tree.parent(seleccion)

        comm = command.get(index1="1.0", index2="end")
        cols, rows = query(conn_manager.get_conexion(seleccion), comm)
        if cols:
            col_width = [len(c) for c in cols]
            result.config(show="headings", columns=cols)
            for i, c in enumerate(cols):
                result.heading(c, text=c)
                result.column(c, width=col_width[i], anchor=W)
            for r in rows:
                val = [r[c] for c in cols]
                result.insert("", "end", values=val)
        else:  
            result.config(show="tree")
            print(rows)
            result.insert("", "end", text=rows)

    def click_derecho(event):
        item_id = tree.identify_row(event.y)
        if item_id:
            tree.selection_set(item_id)
            menu = tk.Menu(tree, tearoff=0)
            if "_tab" in item_id:
                menu.add_command(label="Crear tabla")
                if "_tab_" in item_id:
                    n, item = item_id.split("_tab_")
                    menu.add_command(label="Ver DDL", command=lambda: gen_ddl(item, "table", n))
                menu.post(event.x_root, event.y_root)
            if "_vis" in item_id:
                menu.add_command(label="Crear vista")
                if "_vis_" in item_id:
                    n, item = item_id.split("_vis_")
                    menu.add_command(label="Ver DDL", command=lambda: gen_ddl(item, "view", n))
                menu.post(event.x_root, event.y_root)
            if "_proc_" in item_id:
                n, item = item_id.split("_proc_")
                menu.add_command(label="Ver DDL", command=lambda: gen_ddl(item, "procedure", n))
                menu.post(event.x_root, event.y_root)
            if "_func_" in item_id:
                n, item = item_id.split("_func_")
                menu.add_command(label="Ver DDL", command=lambda: gen_ddl(item, "function", n))
                menu.post(event.x_root, event.y_root)
            if "_trig_" in item_id:
                n, item = item_id.split("_trig_")
                menu.add_command(label="Ver DDL", command=lambda: gen_ddl(item, "trigger", n))
                menu.post(event.x_root, event.y_root)


        return

    def gen_ddl(item, type, con):
        sql = f"SHOW CREATE {type.upper()} `{item}`"
        cursor = conn_manager.get_conexion(con).cursor()
        cursor.execute(sql)
        
        ddl = cursor.fetchall()
        command.delete("1.0", tk.END)
        if type in ("procedure", "function", "trigger"):
            command.insert("1.0", ddl[0][2])
        else:
            command.insert("1.0", ddl[0][1])
        notebook.select(sql_editor)
        return
    
    def ver_datos(item, con):
        for item in result.get_children():
            result.delete(item)

        notebook.select(sql_editor)
        cols, rows = query(conn_manager.get_conexion(con), f"SELECT * FROM {item}")
        col_width = [len(c) for c in cols]
        result.config(show="headings", columns=cols)
        for i, c in enumerate(cols):
            result.heading(c, text=c)
            result.column(c, width=col_width[i], anchor=W)
        for r in rows:
            val = [r[c] for c in cols]
            result.insert("", "end", values=val)
        
        

    # -----TKINTER CODE BLOCKS--------
    root = tk.Tk()
    root.title("My Database Manager")
    root.geometry("1000x600")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

    mainframe.columnconfigure(0, weight=0)  
    mainframe.columnconfigure(1, weight=1) 
    mainframe.rowconfigure(0, weight=1) 
    
    mainframe.grid_columnconfigure(1, minsize=750)
    mainframe.grid_rowconfigure(0, minsize=500)

    # Barra de herramientas
    menubar = tk.Menu(root)
    root.config(menu = menubar)

    menu_conexion = tk.Menu(menubar, tearoff=0)
    menu_conexion.add_command(
        label='Crear conexión',
        command=add_connection
    )
    menu_conexion.add_command(
        label='Editar conexión',
        command=edit_connection,
        state='disabled'
    )
    menu_conexion.add_command(
        label='Borrar conexión',
        command=del_connection,
        state='disabled'
    )
    menu_conexion.add_command(
        label="Exportar a PostGre",
        command=exp_connection,
        state='disabled'
    )

    menubar.add_cascade(label="Conexión", menu=menu_conexion)
    
    def actualizar_menu(event=None):
        seleccion = tree.selection()
        if seleccion:
            command.config(state="normal")
            for con in conn_manager.conexiones:
                if seleccion[0] == con:
                    menu_conexion.entryconfig("Editar conexión", state="normal")
                    menu_conexion.entryconfig("Borrar conexión", state="normal")
                    menu_conexion.entryconfig("Exportar a PostGre", state="normal")
                else:
                    menu_conexion.entryconfig("Borrar conexión", state="disabled")
                    menu_conexion.entryconfig("Editar conexión", state="disabled")  
                    menu_conexion.entryconfig("Exportar a PostGre", state="disabled")

    # Barra lateral de objetos
    sideframe = ttk.Frame(mainframe, width=200, height=500)
    sideframe.grid(column=0, row=0, sticky=(N, W, S), padx=(0,5))
    sideframe.grid_propagate(False)


    tree = ttk.Treeview(sideframe, show="tree")
    tree.pack(fill="both", expand=True)
    tree.bind("<Double-1>", on_double_click)
    tree.bind("<<TreeviewSelect>>", actualizar_menu)
    tree.bind("<Button-3>", click_derecho)

    # Notebook Principal
    primaryframe = ttk.Frame(mainframe, padding="2 2 2 2", relief="groove", borderwidth=2)
    primaryframe.grid(column=1, row=0, sticky=(N, E, W, S), padx=(5,0))
    primaryframe.pack_propagate(False)

    notebook = ttk.Notebook(primaryframe)
    notebook.pack(fill="both", expand=True)

    
    sql_editor = ttk.Frame(notebook)
    notebook.add(sql_editor, text="SQL Editor")
    sql_editor.rowconfigure(0, weight=1, minsize=350)
    sql_editor.rowconfigure(2, weight=1, minsize=150)
    sql_editor.columnconfigure(1, weight=1)
    sql_editor.columnconfigure(0, weight=1)

    result = ttk.Treeview(sql_editor, selectmode="none")
    result.grid(row=0, column=0, columnspan=2, sticky=(N, S, E, W),pady=(2, 1), padx=(2,2))

    ttk.Label(sql_editor, text="Consola SQL: ").grid(row=1, column=0, sticky=W)
    command = tk.Text(sql_editor, state="disabled")
    command.grid(row=2, column=0, sticky=(N, S, E, W),pady=(2, 1), padx=(2,2))


    execute = ttk.Button(sql_editor, text="EJECUTAR", command=ejecutar_en_conexion)
    execute.grid(row=2, column=1, sticky=(N, E, W),pady=(2, 1), padx=(2,2))

    root.mainloop()