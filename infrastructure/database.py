from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash

# Crear una instancia de SQLAlchemy
db = SQLAlchemy()

# Definir el modelo de Nodo
from flask_sqlalchemy import SQLAlchemy

# Crear una instancia de SQLAlchemy
db = SQLAlchemy()

# Definir el modelo de Usuario
class UsuarioModel(db.Model):
    """Modelo de la tabla usuarios en la base de datos."""
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    organigramas = db.relationship('OrganigramaModel', back_populates='username', cascade="all, delete")


    def __repr__(self):
        return f"UsuarioModel(id={self.id}, nombre={self.nombre}, email={self.correo})"

# Definir el modelo de Organigrama

class OrganigramaModel(db.Model):
    """Modelo de la tabla organigramas en la base de datos."""
    __tablename__ = 'organigramas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    # Relación con el modelo Usuario
    username = db.relationship('UsuarioModel', back_populates='organigramas')

    # Relación con el modelo Nodo
    nodos = db.relationship('NodoModel', back_populates='organigrama', cascade="all, delete")

    def __repr__(self):
        return f"OrganigramaModel(id={self.id}, nombre={self.nombre}, usuario_id={self.usuario_id})"

# Definir el modelo de Nodo
class NodoModel(db.Model):
    """Modelo de la tabla nodos en la base de datos."""
    __tablename__ = 'nodos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    tipo_cargo = db.Column(db.String(100), nullable=False)  
    organigrama_id = db.Column(db.Integer, db.ForeignKey('organigramas.id', ondelete="CASCADE"), nullable=False)
    padre_id = db.Column(db.Integer, db.ForeignKey('nodos.id'), nullable=True)

    # Campos personalizables
    color_bg = db.Column(db.String(7), default="#FFFFFF")  # Color de fondo
    color_border = db.Column(db.String(7), default="#000000")  # Color del borde
    color_text = db.Column(db.String(7), default="#000000")  # Color sdel texto

    # Relación con el modelo Organigrama
    organigrama = db.relationship('OrganigramaModel', back_populates='nodos')

    # Relación con el modelo Nodo (hijos)
    hijos = db.relationship('NodoModel', backref='padre', remote_side=[id], cascade="all, delete")

def init_db(app):
    """
    Inicializa la base de datos con la aplicacion Flask

    :param app: Instancia de la aplicacion Flask.
    """
    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()