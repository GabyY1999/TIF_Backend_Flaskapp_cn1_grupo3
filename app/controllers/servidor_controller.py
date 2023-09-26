from flask import request, jsonify
from ..models.servidores_model import Servidor
from ..models.miembroservidor_model import MiembroServidor

class ServidoresController:

    @classmethod
    def mostrar_todos_servidores(cls):
        try:
            servidores = Servidor.obtener_todos_servidores()
            servidores_serializados = [servidor.serialize() for servidor in servidores]
            return jsonify(servidores_serializados), 200
        except Exception as e:
            print("Error en mostrar_todos_servidores:", e)
            return {"mensaje": "Hubo un error en el servidor"}, 500
    
    @classmethod
    def mostrar_servidor(cls, servidor_id):
        try:
            servidor = Servidor.obtener_servidor_por_id(servidor_id)

            if servidor:
                servidor_serializado = servidor.serialize()
                return jsonify(servidor_serializado), 200
            else:
                return {"mensaje": "Servidor no encontrado"}, 404
        except Exception as e:
            print("Error en mostrar_servidor:", e)
            return {"mensaje": "Hubo un error en el servidor"}, 500

    @classmethod
    def crear_servidor(cls):
        try:
            data = request.json
            nombre_servidor = data.get('nombre_servidor', '')
            # Crear el servidor
            created_server = Servidor.crear_servidor(nombre_servidor)
            if created_server:
                # Obtener el ID del servidor recién creado
                server_id = created_server  # Reemplaza esto con la forma real de obtener el ID
                # Obtener el ID del usuario actual, suponiendo que estás autenticado
                user_id = data.get('user_id',None)
                # Definir el rol para el creador del servidor (puedes ajustarlo según tus necesidades)
                creador_rol_id = "creador"  # Reemplaza esto con el ID del rol "creador" en tu base de datos
                # Crear el registro en miembroServidor
                MiembroServidor.crear_miembro_servidor(user_id, server_id, creador_rol_id)
                Canal.crear_canal(server_id,"bienvenida")
                return {'message': 'Servidor creado con éxito'}, 201
            else:
                return {'message': 'No se pudo crear el servidor'}, 500
        except Exception as e:
            print("Error en crear_servidor:", e)
            return {'message': 'Hubo un error en el servidor'}, 500

    @classmethod
    def eliminar_servidor(cls, servidor_id):
        try:
            deleted_successfully = Servidor.eliminar_servidor(servidor_id)

            if deleted_successfully:
                return {"message": "Servidor eliminado correctamente"}, 204
            else:
                return {"message": "No se encontró el servidor o hubo un problema al eliminarlo"}, 404
        except Exception as e:
            print("Error en eliminar_servidor:", e)
            return {"message": "Hubo un error en el servidor"}, 500
    
    @classmethod
    def unirse_a_servidor(cls, servidor_id):
        print("Llego a unirse_servidor")
        resul=0
        try:
        # Obtén los datos de la solicitud JSON
            data = request.json
            user_id = data.get('user_id', None)
            print("SERVIDOR ID:", servidor_id, "USUARIO ID:", user_id)
            resul = MiembroServidor.verificar_usuario(user_id, servidor_id)
            print(resul)
            if resul:
                print("Error al unirse al servidor: Usuario ya registrado en el servidor.")
                return {'message': 'El usuario ya está registrado en el servidor'}, 400
            else:
            # Verificar si el usuario se encuentra en la base de datos MiembroServidor con ese server_id
            # Si no lo encuentra, lo agrega como miembro
                if MiembroServidor.crear_miembro_servidor(user_id, servidor_id, "miembro"):
                    return {'message': 'Usuario asignado al servidor con éxito'}, 200
                else:
                    return {'message': 'Hubo un error en el servidor'}, 500
        except Exception as e:
            print("Error al unirse al servidor:", str(e))
            return {'message': 'Hubo un error en la solicitud'}, 500

    @classmethod
    def obtener_servidores_usuario(cls,user_id):
        print("Llego asta obtener servidores usuario")
        print(user_id)
        servidores = MiembroServidor.obtener_servidores_del_usuario(user_id)
        print(servidores)
        # Luego, convierte la lista de servidores en un formato JSON
        servidores_json = [{'nombre': servidor['nombre'], 'serverID': servidor['serverID']} for servidor in servidores]
        #print("Servidores del usuario",servidores_json)
        # Devuelve la respuesta como JSON
        return jsonify(servidores_json), 200
