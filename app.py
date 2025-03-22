from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from infrastructure.database import db, init_db
from application.nodo_routes import nodo_bp
from application.oranigrama_routes import organigrama_bp
from application.usuario_routes import auth_bp

def create_app():
    """Factory function para crear la aplicacion flask"""
    # carga de variables de entorno
    load_dotenv()

    # Crear la aplicacion Flask
    app = Flask(__name__)

    # Configuracion de la clave secreta jwt
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Inicializar JWT
    jwt = JWTManager(app)

    # Configuracion de la aplicacion
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Inicializar la base de datos
    init_db(app) 
    migrate = Migrate(app, db)

    # Registrar blueprints (rutas)
    app.register_blueprint(auth_bp, use_prefix='/api')
    app.register_blueprint(organigrama_bp, use_prefix='/api')
    app.register_blueprint(nodo_bp, use_prefix='/api')

    CORS(app)

    return app

# iniciar applicacion
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)