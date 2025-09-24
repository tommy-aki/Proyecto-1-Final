def query(conexion, query):
    try:    
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(query)

        if cursor.description:  # SELECT
            try:
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                cursor.close()
                return columns, result
            except Exception as e:
                cursor.close()
                return None, f"Error al obtener resultados: {str(e)}"
        else:  # INSERT, UPDATE, DELETE
            try:
                conexion.commit()
                affected = cursor.rowcount
                q = cursor.statement
                cursor.close()
                return None, f"Query {q} ejecutado con {affected} filas afectadas"
            except Exception as e:
                cursor.close()
                return None, f"Error al obtener resultados: {str(e)}"
    except Exception as e:
        cursor.close()
        return None, f"Error al obtener resultados: {str(e)}"