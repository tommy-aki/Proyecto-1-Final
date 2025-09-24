import mysql.connector as con

class ConnectionManager:

    def __init__(self):
        self.conexiones = {}


    def conectar(self, host, user, password, db, port):
        nombre = f"{user}@{host}:{port}/{db}"

        try:
            conexion = con.connect(
                host=host,
                user=user,
                password=password,
                database=db,
                port=port
            ) 
            self.conexiones[nombre] = conexion
            return conexion
        except  con.Error as e:
            raise Exception(f"Error de conexion: {e}")
        
    def edit_conexion(self, host, user, password, db, port, nombre):
        self.cerrar_conexion(nombre)
        return self.conectar(host, user, password, db, port)
        
    def get_conexion(self, nombre):
        return self.conexiones.get(nombre)

    def cerrar_conexion(self, nombre):
        if nombre in self.conexiones:
            self.conexiones[nombre].close()
            del self.conexiones[nombre]

    def listar_conexiones(self):
        return list(self.conexiones.keys())
    
    def cerrar_conexion(self, nombre):
        conn = self.conexiones[nombre]
        conn.close()

    def cerrar_todas(self):
        for conn in self.conexiones.values():
            conn.close()
        self.conexiones.clear()