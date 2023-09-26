from flask import request, jsonify
from ..models.canal_model import Canal
from ..models.servidores_model import Servidor



class CanalController:

    @classmethod
    def obtener_canales_servidor(cls, servidor_id):
        print("Llego asta obtener canales servidor")
        try:
            canales=Canal.obtener_canales(servidor_id)
            #print(canales)
            # Devuelve una lista de canales en formato JSON
            #canales = [{'nombre': 'Canal 1'}, {'nombre': 'Canal 2'}]  # Reemplaza con los canales reales
            return jsonify(canales), 200
        except Exception as e:
            # Manejo de errores
            response = {'message': 'Error al obtener los canales del servidor'}
            return jsonify(response), 500

    @classmethod    
    def crear_canal(cls):
        try:
            data = request.json
            nombre_canal = data.get('nombre_canal')
            servidor_id = int(data.get('servidor_id'))#servidor_id lo obtiene como un string
            #print("DATOS OBTENIDOS PARA CREAR CANAL:", nombre_canal, servidor_id)
            # Llama a la función para crear el canal
            resul = Servidor.agregar_canal(servidor_id, nombre_canal)
            print (resul)
        #print(resul)
            #if resul:
                # Devuelve una respuesta JSON exitosa si el canal se crea con éxito
            return jsonify({'message': 'Canal creado con éxito'}), 200
            #else:
                # Devuelve una respuesta JSON con un mensaje de error si hay un problema
            #    return jsonify({'message': 'Error al crear el canal'}), 500
        except Exception as e:
            # Manejo de errores más genérico
            return jsonify({'message': 'Error en crear canal'}), 500