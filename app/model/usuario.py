from app.routes.BaseDatos import DatabaseConnection
from passlib.hash import sha256_crypt

class Usuario:
    def __init__(self, nombreusuario, nombre, apellido, correo, contraseña, fecha_nacimiento, imagen=None):
        self.nombreusuario = nombreusuario
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contraseña = contraseña
        self.fecha_nacimiento = fecha_nacimiento
        self.imagen = imagen

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
    def iniciar_sesion(correo, contraseña):
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
    
    @staticmethod
    def obtener_servidores_del_usuario(user_id):
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()

            query = "SELECT servidor_id FROM miembroServidor WHERE usuario_id = %s"
            cursor.execute(query, (user_id,))
            servidores = [row[0] for row in cursor.fetchall()]
            if len(servidores)==0:
                return None
            else:
                return servidores
        except Exception as e:
            print("Error al obtener servidores del usuario:", e)
            return []