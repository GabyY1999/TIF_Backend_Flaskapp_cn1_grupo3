from app import create_app
from app.BaseDatos import DatabaseConnection  # Importa la clase DatabaseConnection
from configuracion import credenciales

# Crea una instancia de la aplicación Flask
app = create_app()

if __name__ == "__main__":
    # Llama al método create_if_not_exists para crear la base de datos y tablas si no existen
    DatabaseConnection.set_config(credenciales)
    DatabaseConnection.create_if_not_exists()
    app.run()
