from ..BaseDatos import DatabaseConnection

class Canal:
    def __init__(self, canal_id, server_id, nombre):
        self.canal_id = canal_id
        self.server_id = server_id
        self.nombre = nombre

    @classmethod
    def obtener_canales(cls, servidor_id):
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            query="SELECT * FROM canales WHERE serverID = %s"
            cursor.execute(query, (servidor_id,))
            column_names = [desc[0] for desc in cursor.description]  # Obtiene los nombres de las columnas
            resultados = cursor.fetchall()
            lista_de_diccionarios = [dict(zip(column_names, row)) for row in resultados]
            print("LOS CANALES SON:", lista_de_diccionarios)
            return lista_de_diccionarios
        except Exception as e:
            # Manejo de errores
            print("Error al obtener los canales:", e)
            return []
        
    @classmethod
    def crear_canal(cls, servidor_id, nombre_canal):
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO canales(serverID, nombre) VALUES (%s, %s)"
            val=(servidor_id, nombre_canal)
            cursor.execute(query, (servidor_id, nombre_canal))
            conn.commit()
            #DatabaseConnection.insert_data(query, val)
            return True
        except Exception as e:
            print("Error en crear canal",e)
            # Manejo de errores
            return False

    # ...
