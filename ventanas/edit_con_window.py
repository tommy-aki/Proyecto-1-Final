import tkinter as tk
from tkinter import N, E, S, W
from tkinter import messagebox
from tkinter import ttk
from db.connection import ConnectionManager as cm

def edit_window(parent, conn_manager, nombre, callback):
    def edit():
        db = entry_db.get()
        if db == "":
            messagebox.showerror("Error", "Especificar la base de datos")
            root.lift()
        else:
            try:
                host = entry_host.get()
                user = entry_user.get()
                password = entry_pass.get()
                port = int(entry_port.get()) if entry_port.get() else 3306

                # Crear conexión usando el manager que vino de MainWindow
                new_nombre = f"{user}@{host}:{port}/{db}"
                conn_manager.edit_conexion(host, user, password, db, port, nombre)

                messagebox.showinfo("Conexión", f"Conectado con éxito a {new_nombre}")

                # Llamar callback para actualizar UI en MainWindow
                callback(new_nombre, db)

                root.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                root.lift()

    user, nom1 = nombre.split("@", 1)
    host, nom2 = nom1.split(":", 1)
    port, db = nom2.split("/", 1)

    root = tk.Tk()
    root.title("Conexión MySQL")
    root.geometry("300x250")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    ttk.Label(mainframe, text="Host:", padding="5 0 0 0").grid(column=1, row=1, sticky=E)
    entry_host = ttk.Entry(mainframe, width=32)
    entry_host.insert(0, host)
    entry_host.grid(column=2, row=1, sticky=W, pady=7)

    ttk.Label(mainframe, text="Username:", padding="5 0 0 0").grid(column=1, row=2, sticky=E)
    entry_user = ttk.Entry(mainframe, width=32)
    entry_user.insert(0, user)
    entry_user.grid(column=2, row=2, sticky=W, pady=7)

    ttk.Label(mainframe, text="Password:", padding="5 0 0 0").grid(column=1, row=3, sticky=E)
    entry_pass = ttk.Entry(mainframe, width=32)
    entry_pass.grid(column=2, row=3, sticky=W, pady=7)

    ttk.Label(mainframe, text="Database:", padding="5 0 0 0").grid(column=1, row=4, sticky=E)
    entry_db = ttk.Entry(mainframe, width=32)
    entry_db.insert(0, db)
    entry_db.grid(column=2, row=4, sticky=W, pady=7)

    ttk.Label(mainframe, text="Port:", padding="5 0 0 0").grid(column=1, row=5, sticky=E)
    entry_port = ttk.Entry(mainframe, width=32)
    entry_port.insert(0,port)
    entry_port.grid(column=2, row=5, sticky=W, pady=7)

    ttk.Button(mainframe, text="Editar", command=edit).grid(column=2, row=6, sticky=E, pady=7)

    root.mainloop()

