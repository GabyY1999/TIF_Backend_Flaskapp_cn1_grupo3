from ..BaseDatos import DatabaseConnection  # Importa tu clase de conexión a la base de datos
from .canal_model import Canal
from .mensaje_model import Mensaje

class Servidor:
    def __init__(self, serverID, cantUser, nombre):
        self.serverID = serverID
        self.cantUser = cantUser
        self.nombre = nombre

    @classmethod
    def crear_servidor(cls, nombre_servidor):
        try:
            query = "INSERT INTO servidor (nombre, cantUser) VALUES (%s, %s)"  # Agrega un valor predeterminado para cantUser
            val=(nombre_servidor, 1)
            DatabaseConnection.insert_data(query, val)
            servidor_id = DatabaseConnection.obtener_ultimoservidor()  # Obtiene el ID del servidor recién creado
            return servidor_id
        except Exception as e:
            print("Error en crear_servidor:", e)
            return False
    

    @classmethod
    def obtener_todos_servidores(cls):
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM servidor"
            cursor.execute(query)
            servidores = cursor.fetchall()
            return [Servidor(serverID, cantUser, nombre) for serverID, cantUser, nombre in servidores]
        except Exception as e:
            print("Error en obtener_todos_servidores:", e)
            return []

    @classmethod
    def obtener_servidor_por_id(cls, servidor_id):
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM servidor WHERE serverID = %s"
            cursor.execute(query, (servidor_id,))
            servidor = cursor.fetchone()
            print("datos obtenidos del servidor",servidor)
            if servidor:
                return Servidor(servidor[0], servidor[1], servidor[2])
            return None
        except Exception as e:
            print("Error en obtener_servidor_por_id:", e)
            return None

    @classmethod
    def eliminar_servidor(cls, servidor_id):
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            query = "DELETE FROM servidor WHERE serverID = %s"
            cursor.execute(query, (servidor_id,))
            conn.commit()
            return True
        except Exception as e:
            print("Error en eliminar_servidor:", e)
            return False

    def serialize(self):
        return {
            "serverID": self.serverID,
            "cantUser": self.cantUser,
            "nombre": self.nombre
        }
    
    @classmethod
    def asignar_usuario(cls, servidor_id, usuario_id, rol_id):
        try:
            query = "INSERT INTO usuarioservidor (usuario_id, servidor_id, rolID) VALUES (%s, %s, %s)"
            val=(usuario_id, servidor_id, rol_id)
            DatabaseConnection.insert_data(query, val)
            return True
        except Exception as e:
            print("Error al asignar usuario al servidor:", e)
            return False

    @classmethod
    def agregar_canal(cls,servidor_id,nombre_canal):
        print("Llego a servidor_model")
        #Canal(1,servidor_id,nombre_canal)
        resul = Canal.crear_canal(servidor_id, nombre_canal)
        return resul
    
    @classmethod
    def obtener_mensajes(cls,chanel_id):
        lista=Mensaje.lista_mensaje(chanel_id)
        return lista