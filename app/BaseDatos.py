import mysql.connector
from mysql.connector import Error,errors
from configuracion import credenciales


class DatabaseConnection:
    _connection = None
    _config = None

    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            cls._connection = mysql.connector.connect(**cls._config)
        return cls._connection

    @classmethod
    def set_config(cls, config):
        cls._config = config

    @classmethod
    def execute_query(cls, query, params=None):
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor

    @classmethod
    def fetch_all(cls, query, params=None):
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    @classmethod
    def fetch_one(cls, query, params=None):
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

    @classmethod
    def close_connection(cls):
        if cls._connection is not None:
            cls._connection.close()
            cls._connection = None

    @classmethod
    def insert_data(cls, query, params):
        conn = cls.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            print("Datos insertados correctamente.")
        except Error as err:
            print("Error al insertar datos:", err)
        finally:
            cursor.close()

    # Ejemplo de uso:
    # query = "INSERT INTO tabla (columna1, columna2) VALUES (%s, %s)"
    # params = ("valor1", "valor2")
    # DatabaseConnection.insert_data(query, params)

    @classmethod
    def delete_data(cls, query, params=None):
        conn = cls.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, params)
            conn.commit()
            print("Datos eliminados correctamente.")
        except Error as err:
            print("Error al eliminar datos:", err)
        finally:
            cursor.close()

    # Ejemplo de uso:
    # query = "DELETE FROM tabla WHERE columna = %s"
    # params = ("valor_a_eliminar",)
    # DatabaseConnection.delete_data(query, params)

    @classmethod
    def obtener_ultimoservidor(cls):
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT serverID FROM servidor ORDER BY serverID DESC LIMIT 1")
            last_server = cursor.fetchone()
            if last_server:
                return last_server[0]
            else:
                return None
        except Exception as e:
            print("Error al obtener el último servidor:", e)
            return None


    @classmethod
    def create_if_not_exists(cls):
        conn = None  # Inicializa la variable conn aquí
        try:
        # Utiliza la clase DatabaseConnection para obtener la conexión
            DatabaseConnection.set_config(credenciales)
            conn = cls.get_connection()
            cur = conn.cursor()

        # Intenta seleccionar la base de datos existente
            cur.execute("USE %s" % credenciales['database'])

        # Si llega aquí sin errores, la base de datos ya existe
            print("La base de datos ya existe.")
        except Error as err:
        # Si se produce un error al seleccionar la base de datos, significa que no existe
            print("La base de datos no existe. Se creará ahora...")
            if conn is None:
            # Si no se ha establecido una conexión, intenta crear una nueva
                conn = mysql.connector.connect(user=credenciales['user'], password=credenciales['password'], host=credenciales['host'])

        # Crea la base de datos
            create_database = "CREATE DATABASE IF NOT EXISTS %s" % credenciales['database']
            cur = conn.cursor()
            cur.execute(create_database)
            cur.execute("USE %s" % credenciales['database'])
        # Crea las tablas necesarias aquí
            create_table_usuario = """CREATE TABLE IF NOT EXISTS usuario (
                userID INT AUTO_INCREMENT PRIMARY KEY,
                nombreusuario VARCHAR(255) NOT NULL,
                nombre VARCHAR(255) NOT NULL,
                apellido VARCHAR(255) NOT NULL,
                correo VARCHAR(255) NOT NULL,
                contraseña VARCHAR(2000) NOT NULL,
                fecha_nacimiento DATE NOT NULL,
                imagen BLOB NULL
            )"""
            # Agrega aquí los usuario predeterminados que deseas insertar
            default_usuario = [
                ("Bob67", "Bob", "Perez", "Bobi78@hotmail.com", "Bobii89", "1990-04-10"),
                ("An@", "Ana", "Cruz", "Ani10@gmail.com", "Ana909", "1990-05-10"),
                ("Kaladin45", "Kaladin", "Rasputin", "KalakRas10@hotmail.com", "Kali10", "1990-10-08"),
            ] 

            create_table_servidor = """CREATE TABLE IF NOT EXISTS servidor (
                serverID INT AUTO_INCREMENT PRIMARY KEY,
                cantUser INT,
                nombre VARCHAR(255) NOT NULL
            )"""

            # Agrega aquí los servidores predeterminados que deseas insertar
            default_servers = [
                (100, 'Literatura Fantastica'),
                (50, 'Locura Cinematografica'),
                (200, 'Relatos de Viaje'),
                (100, 'Salud y Bienestar'),
                (60, 'Central de Videojuegos'),
                (20, 'Fanaticos del Deporte'),
                (20, 'Caos Musical'),
            # Agrega más servidores predeterminados según sea necesario
            ]

            create_table_miembroServidor="""CREATE TABLE IF NOT EXISTS miembroServidor (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT,
                servidor_id INT,
                rol VARCHAR(60) NOT NULL,
                fecha_unirse TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuario (userID),
                FOREIGN KEY (servidor_id) REFERENCES servidor (serverID)
            )"""
            create_table_canales = """CREATE TABLE IF NOT EXISTS canales (
                canalID INT AUTO_INCREMENT PRIMARY KEY,
                serverID INT NOT NULL,
                nombre VARCHAR(255) NOT NULL,
                FOREIGN KEY (serverID) REFERENCES servidor (serverID)
            )"""
            default_canal1= [
                (1, 'Club de Lectura'),
                (1, 'Escritores emergentes'),
                (1, 'Recomendaciones'),
            ]
            default_canal2 = [
                (2, 'Salud Mental y Felicidad'),
                (2, 'Cine en Fantasía'),
            ]
            create_table_mensaje ="""CREATE TABLE IF NOT EXISTS mensaje(
                mensajeID INT AUTO_INCREMENT PRIMARY KEY,
                canalID INT,
                userID INT,
                contenido VARCHAR(500) NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (canalID) REFERENCES canales (canalID),
                FOREIGN KEY (userID) REFERENCES usuario (userID)
            )"""
            cur.execute(create_table_usuario)
            cur.execute(create_table_servidor)
            cur.execute(create_table_miembroServidor)
            cur.execute(create_table_canales)
            cur.execute(create_table_mensaje)
            # Inserta los servidores predeterminados en la tabla servidor
            insert_default_servers = "INSERT INTO servidor (cantUser, nombre) VALUES (%s, %s)"
            insert_default_usuario = "INSERT INTO usuario (nombreusuario, nombre,apellido, correo,contraseña,fecha_nacimiento) VALUES (%s, %s, %s,%s,%s,%s)"
            insert_default_canal1 = "INSERT INTO canales (serverID,nombre) VALUES (%s, %s)"
            insert_default_canal2 = "INSERT INTO canales (serverID,nombre) VALUES (%s, %s)"
            cur.executemany(insert_default_servers, default_servers)
            cur.executemany(insert_default_usuario, default_usuario)
            cur.executemany(insert_default_canal1, default_canal1)
            cur.executemany(insert_default_canal2, default_canal2)
            conn.commit()
            print("Base de datos y tablas creadas exitosamente.")
        finally:
            if conn is not None:
                DatabaseConnection.close_connection()

    # Ejemplo de uso:
    # DatabaseConnection.set_config(config)
    # conn = DatabaseConnection.conectar()
