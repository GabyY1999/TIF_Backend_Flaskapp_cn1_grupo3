from flask import Flask
from configuracion import credenciales
from configuracion import SECRET_KEY  # Importa la clave secreta desde tu archivo de configuración
from .controllers.auth import auth  # Importa tu Blueprint de autenticación

def create_app():
    """Crea y configura la aplicación de Flask"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config.from_object(credenciales)

    # Registra tus Blueprints aquí
    app.register_blueprint(auth)
    return app

