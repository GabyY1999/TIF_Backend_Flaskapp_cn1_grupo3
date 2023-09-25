from ..BaseDatos import DatabaseConnection

class Mensaje:
    def __init__(self, mensajeID, canalID, userID,contenido,fecha):
        self.mensajeID = mensajeID
        self.canalID = canalID
        self.userID = userID
        self.contenido=contenido
        self.fecha=fecha


    @classmethod
    def lista_mensaje(canal_id):
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM canales WHERE canalID = %s"
            cursor.execute(query, (canal_id,))
            mensajes = [row[0] for row in cursor.fetchall()]
            conn.commit()
            cursor.close()
            conn.close()
            return mensajes
        except Exception as e:
            return []