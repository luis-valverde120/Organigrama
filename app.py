from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager 
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
from infrastructure.database import db, init_db
from application.nodo_routes import nodo_bp
from application.oranigrama_routes import organigrama_bp
from application.usuario_routes import usuario_bp 

def create_app():
    """Factory function para crear la aplicacion flask"""
    # carga de variables de entorno
    load_dotenv()

    # Crear la aplicacion Flask
    app = Flask(__name__)

    # Configuracion de la clave secreta jwt
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # Asegúrate de que esta clave esté definida

    # Inicializar JWT
    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)

    # Configuracion de la aplicacion
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Inicializar la base de datos
    init_db(app) 
    migrate = Migrate(app, db)

    # Registrar blueprints (rutas)
    app.register_blueprint(usuario_bp, url_prefix='/api')
    app.register_blueprint(organigrama_bp, url_prefix='/api')
    app.register_blueprint(nodo_bp, url_prefix='/api')

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    return app

# iniciar applicacion
if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0",  port=port)