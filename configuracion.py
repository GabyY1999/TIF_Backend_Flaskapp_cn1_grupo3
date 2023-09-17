import secrets
import string
credenciales = {
    'host': 'localhost',
    'port': 3306,
    'database': 'proyecto',
    'user': 'root',
    'password': 'Trapos@1987'
}
# Longitud de la clave secreta
length = 24  # Puedes ajustar la longitud según tus necesidades

# Generar una clave secreta aleatoria
SECRET_KEY = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(length))
