
class MiembroServidor:
    def __init__(self, usuario_id, servidor_id, fecha):
        self.usuario_id = usuario_id
        self.servidor_id = servidor_id
        self.fecha= fecha

    # Puedes agregar métodos adicionales según sea necesario, como para obtener la fecha de unión.

    @staticmethod
    def registrar_miembro(usuario_id, servidor_id):
        # Aquí puedes implementar la lógica para registrar un usuario como miembro de un servidor.
        # Puedes usar la fecha actual para la columna `fecha_unirse`.
        pass

    @staticmethod
    def obtener_miembros_del_servidor(servidor_id):
        # Aquí puedes implementar la lógica para obtener todos los miembros de un servidor específico.
        pass
