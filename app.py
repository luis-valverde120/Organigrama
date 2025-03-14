from flask import Flask
from dotenv import load_dotenv
import os
from controllers import organigrama_blueprint

# Cargar variables de entorno
load_dotenv()

# iniciar la aplicaicon Flask
app = Flask(__name__)

# configuracion basica SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv['SECRET_KEY']

# inicializar la base de datos
init_db(app)

# Registrar blueprints (rutas)
app.register_blueprint(organigrama_blueprint)

# iniciar applicacion
if __name__ == '__main__':
    app.run(debug=True)