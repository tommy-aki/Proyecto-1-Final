import tkinter as tk
from tkinter import N, E, S, W
from tkinter import messagebox
from tkinter import ttk
from db.connection import ConnectionManager as cm
from db.export import export
import psycopg
from psycopg.rows import dict_row

def sync_window(conexion):
    def create_if_not_exists(dbname, user, password, host="localhost", port=5432):
        with psycopg.connect(
            dbname="postgres", user=user, password=password, host=host, port=port
        ) as conn:
            conn.autocommit = True  # Necesario para CREATE DATABASE
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,)
                )
                exists = cur.fetchone()
                if not exists:
                    cur.execute(f'CREATE DATABASE "{dbname}";')
                    print(f"Base de datos '{dbname}' creada.")
                else:
                    print(f"Base de datos '{dbname}' ya existe.")
        conn_target = psycopg.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        return conn_target
    
    def connect():
        db = entry_db.get()
        if db == "":
            messagebox.showerror("Error", "Especificar la base de datos")
            root.lift()
        try:
            host = entry_host.get()
            user = entry_user.get()
            password = entry_pass.get()
            port = int(entry_port.get()) if entry_port.get() else 5432

            conn_pg = create_if_not_exists(db, user, password, host, port)

            export(conexion, conn_pg)
            root.destroy()
            conn_pg.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            root.lift()

    root = tk.Tk()
    root.title("Conexión PostgreSQL")
    root.geometry("300x250")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    ttk.Label(mainframe, text="Insertar datos de conexión PostGreSQL", padding="5 0 0 0").grid(column=1, row=0, columnspan=2, sticky=E)

    ttk.Label(mainframe, text="Host:", padding="5 0 0 0").grid(column=1, row=1, sticky=E)
    entry_host = ttk.Entry(mainframe, width=32)
    entry_host.grid(column=2, row=1, sticky=W, pady=7)

    ttk.Label(mainframe, text="Username:", padding="5 0 0 0").grid(column=1, row=2, sticky=E)
    entry_user = ttk.Entry(mainframe, width=32)
    entry_user.grid(column=2, row=2, sticky=W, pady=7)

    ttk.Label(mainframe, text="Password:", padding="5 0 0 0").grid(column=1, row=3, sticky=E)
    entry_pass = ttk.Entry(mainframe, width=32)
    entry_pass.grid(column=2, row=3, sticky=W, pady=7)

    ttk.Label(mainframe, text="Database:", padding="5 0 0 0").grid(column=1, row=4, sticky=E)
    entry_db = ttk.Entry(mainframe, width=32)
    entry_db.grid(column=2, row=4, sticky=W, pady=7)

    ttk.Label(mainframe, text="Port:", padding="5 0 0 0").grid(column=1, row=5, sticky=E)
    entry_port = ttk.Entry(mainframe, width=32)
    entry_port.grid(column=2, row=5, sticky=W, pady=7)

    ttk.Button(mainframe, text="Conectar", command=connect).grid(column=2, row=6, sticky=E, pady=7)

    root.mainloop()