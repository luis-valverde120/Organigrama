from flask import Flask
from dotenv import load_dotenv
import os
from infrastructure.database import init_db
from application.controllers import organigrama_blueprint

def create_app():
    """Factory function para crear la aplicacion flask"""
    # carga de variables de entorno
    load_dotenv()

    # Crear la aplicacion Flask
    app = Flask(__name__)

    # Configuracion de la aplicacion
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Inicializar la base de datos
    init_db(app)

    # Registrar blueprints (rutas)
    app.register_blueprint(organigrama_blueprint)

    return app

# iniciar applicacion
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)