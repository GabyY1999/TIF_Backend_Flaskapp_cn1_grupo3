from ...BaseDatos import DatabaseConnection
from passlib.hash import sha256_crypt
from ..miembroservidor_model import MiembroServidor

class Usuario:
    def __init__(self, **kwargs):
        """Constructor de la clase Usuario. Recibe un conjunto de argumentos con nombre (**kwargs),
        puede tomar múltiples argumentos clave-valor para inicializar los atributos de la clase.
        A continuación, se inicializan varios atributos de la clase a partir de los valores proporcionados en los kwargs.
        """
        self.userID = kwargs.get('userID')
        self.nombreusuario = kwargs.get('nombreusuario')
        self.nombre = kwargs.get('nombre')
        self.apellido = kwargs.get('apellido')
        self.correo = kwargs.get('correo')
        self.contraseña = kwargs.get('contraseña')
        self.fecha_nacimiento = kwargs.get('fecha_nacimiento')
        self.imagen = kwargs.get('imagen', "")

    def serialize(self):
        """Convierte la instancia de la clase en un diccionario.
        Al serializar un objeto Python a JSON, se convierte en una cadena JSON
        que luego se puede enviar a través de una solicitud HTTP"""

        return {
            "userID": self.userID,
            "nombreusuario": self.nombreusuario,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "correo": self.correo,
            "contraseña": self.contraseña,
            "fecha_nacimiento": self.fecha_nacimiento,
            "imagen": self.imagen,
        }

    @staticmethod
    def iniciar_sesion(correo,contraseña):
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM usuario WHERE correo = %s"
            cursor.execute(query, (correo,))
            user = cursor.fetchone()
            if user:
                stored_password_hash = user[5]  # Asegúrate de que el índice sea correcto
            # Verifica la contraseña almacenada en la base de datos con la proporcionada
                if sha256_crypt.verify(contraseña, stored_password_hash):
                # Devuelve los datos del usuario si la contraseña es correcta
                    return {
                        'user_id': user[0],
                        'user_name': user[1],
                        'email': user[4]
                    }
            return None  # Credenciales incorrectas
        except Exception as e:
            print("Error al iniciar sesión:", e)
            return None  # Error en el inicio de sesión
        
    @staticmethod
    def registrar_usuario(nombreusuario, nombre, apellido, correo, contraseña, fecha_nacimiento, imagen=None):
        # Hashea la contraseña antes de almacenarla en la base de datos
        contraseña = sha256_crypt.hash(contraseña)
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()

            query = "INSERT INTO usuario(nombreusuario, nombre, apellido, correo, contraseña, fecha_nacimiento, imagen) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (nombreusuario, nombre, apellido, correo, contraseña, fecha_nacimiento, imagen))
            conn.commit()
            return True  # Registro exitoso
        except Exception as e:
            print("Error al registrar usuario:", e)
            return False  # Error en el registro
    
    @staticmethod
    def obtener_usuario_por_correo(correo):
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()

            query = "SELECT * FROM usuario WHERE correo = %s"
            cursor.execute(query, (correo,))
            user = cursor.fetchone()

            if user:
            # Crear y devolver una instancia de Usuario con los datos obtenidos de la base de datos
                return Usuario(
                    nombreusuario=user[1],
                    nombre=user[2],
                    apellido=user[3],
                    correo=user[4],
                    contraseña=user[5],
                    fecha_nacimiento=user[6],
                    imagen=user[7] if len(user) > 7 else None
                )

            return None  # Usuario no encontrado
        except Exception as e:
            print("Error al obtener usuario por correo:", e)
            return None  # Error al obtener el usuario



    @classmethod
    def is_alias_in_use(cls, alias):
        """Verificar si un alias ya está en uso en la base de datos."""

        query = "SELECT userID FROM usuario WHERE nombreusuario = %(nombreusuario)s"
        params = {'nombreusuario': alias}
        
        result = DatabaseConnection.fetch_one(query, params=params)

        if result is not None:
            return True
        return False

    @classmethod
    def is_email_in_use(cls, correo_electronico):
        """Verificar si un correo electrónico ya está en uso en la base de datos."""

        query = "SELECT userID FROM usuario WHERE correo = %(correo)s"
        params = {'correo': correo_electronico}
        
        result = DatabaseConnection.fetch_one(query, params=params)

        if result is not None:
            return True
        return False

    @classmethod
    def get(cls, user):
        """Obtener información detallada de un usuario en la base de datos basándose en su nombre de usuario 'nombreusuario'."""

        query = """SELECT * FROM usuario WHERE nombreusuario = %(nombreusuario)s"""
        params = user.__dict__
        result = DatabaseConnection.fetch_one(query, params=params)

        if result is not None:
            return cls(
                userID=result[0],
                nombreusuario=result[1],
                nombre=result[2],
                apellido=result[3],
                correo=result[4],
                contraseña=result[5],
                fecha_nacimiento=result[6],
                imagen=result[7]
            )
        return None

    @classmethod
    def create_usuario(cls, usuario):
        """Insertar un nuevo usuario en la base de datos."""
        
        query = """INSERT INTO usuario (nombreusuario, nombre, apellido, correo, contraseña, fecha_nacimiento, imagen) 
        VALUES (%(nombreusuario)s, %(nombre)s, %(apellido)s, %(correo)s, %(contraseña)s, %(fecha_nacimiento)s, %(imagen)s);"""

        params = usuario.__dict__

        result = DatabaseConnection.execute_query(query, params=params)

        if result:
            return True
        else:
            return False

    @classmethod
    def update_usuario(cls, usuario):
        """Modifica un usuario existente en la base de datos."""

        query = """UPDATE usuario SET nombre = %(nombre)s, apellido = %(apellido)s, correo = %(correo)s, 
                   contraseña = %(contraseña)s, fecha_nacimiento = %(fecha_nacimiento)s, imagen = %(imagen)s 
                   WHERE nombreusuario = %(nombreusuario)s"""

        params = usuario.__dict__

        result = DatabaseConnection.execute_query(query, params=params)

        if result:
            return True
        else:
            return False

    @classmethod
    def delete_usuario(cls, nombreusuario):
        """Elimina un usuario existente en la base de datos."""

        query = "DELETE FROM usuario WHERE nombreusuario = %(nombreusuario)s"
        params = {'nombreusuario': nombreusuario}

        result = DatabaseConnection.execute_query(query, params=params)

        if result:
            return True
        else:
            return False

    @classmethod
    def update_password(cls, nombreusuario, new_password):
        """Actualiza la contraseña de un usuario en la base de datos."""

        query = """UPDATE usuario SET contraseña = %(new_password)s WHERE nombreusuario = %(nombreusuario)s"""
        params = {'nombreusuario': nombreusuario, 'new_password': new_password}

        result = DatabaseConnection.execute_query(query, params=params)

        return result

    @classmethod
    def obtener_servidores_del_usuario(cls, usuario_id):
        try:
            # Utiliza la función obtener_servidores_del_usuario de MiembroServidor
            servidores = MiembroServidor.obtener_servidores_del_usuario(usuario_id)
            print(servidores)
            return servidores
        except Exception as e:
            print("Error en obtener_servidores_del_usuario de Servidor:", e)
            return []
    
    
