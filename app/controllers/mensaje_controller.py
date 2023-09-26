from flask import request, jsonify
from ..models.canal_model import Canal


class MensajeController:
    
    
    classmethod
    def obtener_mensajes(cls,chanel_id):
        print(chanel_id)
        print("Llego hasta obtener mensajes")
        try:
            # Supongamos que aquí conectas a tu base de datos y consultas los mensajes del canal correspondiente
            # messages = consulta_a_la_base_de_datos(chanel_id)
        
            # Por ahora, usemos datos de ejemplo
            messages = [
                {"mensaje_id": 1, "autor": "robin", "contenido": "Hola", "fecha_envio": "2023-09-25 19:14:02"},
                {"mensaje_id": 2, "autor": "alice", "contenido": "Hola de nuevo", "fecha_envio": "2023-09-25 19:15:20"},
            # Agrega más mensajes si es necesario
            ]

            return messages
        except Exception as e:
        # Manejo de errores
            return jsonify({'message': 'Error al obtener los mensajes del canal'}), 500