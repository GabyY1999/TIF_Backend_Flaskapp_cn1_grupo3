# miembro_servidor_model.py
from ..BaseDatos import DatabaseConnection
from ..models.servidores_model import Servidor
class MiembroServidor:
    @classmethod
    def crear_miembro_servidor(cls, usuario_id, servidor_id, rol):
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO miembroServidor (usuario_id, servidor_id, rol) VALUES (%s, %s, %s)"
            cursor.execute(query, (usuario_id, servidor_id, rol))
            conn.commit()
            return True
        except Exception as e:
            print("Error en crear_miembro_servidor:", e)
            return False
    # Otros métodos del modelo MiembroServidor si es necesario
    @classmethod
    def obtener_servidores_del_usuario(cls, usuario_id):
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()

        # Paso 1: Obtener los IDs de los servidores a los que pertenece el usuario
            query = "SELECT servidor_id FROM miembroServidor WHERE usuario_id = %s"
            cursor.execute(query, (usuario_id,))
            server_ids = [row[0] for row in cursor.fetchall()]

            # Paso 2: Obtener los detalles completos de los servidores
            servidores = []
            for server_id in server_ids:
            # Utiliza el método obtener_servidor_por_id de la clase Servidor
                server = Servidor.obtener_servidor_por_id(server_id)
                if server:
                # Construye un diccionario con los detalles del servidor
                    server_details = {
                        'serverID': server.serverID,
                        'nombre': server.nombre,
                        'cantUser': server.cantUser,
                    }
                    servidores.append(server_details)
            return servidores
        except Exception as e:
            print("Error en obtener_servidores_del_usuario:", e)
            return []
            
    @classmethod
    def verificar_usuario(cls, user_id, servidor_id):
        """"ESTE METODO SI NO ENCONTRO NINGUN REGISTRO RETORNA FALSE """
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM miembroServidor WHERE usuario_id = %s AND servidor_id = %s;"
            cursor.execute(query, (user_id, servidor_id))
            result = cursor.fetchone()
            # Comprobar si el usuario está registrado en el servidor
            if result is not None:
                return True
            #if result is not None:
            #    return True
            else:
                return False
        except Exception as e:
            print("Error en verificar_usuario:", e)
            return False

