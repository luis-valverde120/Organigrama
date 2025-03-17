from flask_sqlalchemy import SQLAlchemy

# Crear una instancia de SQLAlchemy
db = SQLAlchemy()

# Definir el modelo de Nodo
from flask_sqlalchemy import SQLAlchemy

# Crear una instancia de SQLAlchemy
db = SQLAlchemy()

# Definir el modelo de Nodo
class NodoModel(db.Model):
    """Modelo de la tabla nodos en la base de datos."""
    __tablename__ = 'nodos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)  # Cargo (ejemplo: CEO, Gerente, etc.)
    tipo_cargo = db.Column(db.String(50), nullable=False)  # 'directo' o 'asesoria'
    padre_id = db.Column(db.Integer, db.ForeignKey('nodos.id'))  # Clave foránea

    # Relación recursiva para representar la jerarquía
    hijos = db.relationship(
        'NodoModel',
        backref=db.backref('padre', remote_side=[id]),  # Referencia al padre
        foreign_keys=[padre_id]  # Especifica la columna de la clave foránea
    )

    def __repr__(self):
        return f"NodoModel(id={self.id}, nombre={self.nombre}, titulo={self.titulo}, tipo_cargo={self.tipo_cargo})"


def init_db(app):
    """
    Inicializa la base de datos con la aplicacion Flask

    :param app: Instancia de la aplicacion Flask.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()