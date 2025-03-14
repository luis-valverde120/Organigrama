from flask_sqlalchemy import SQLAlchemy

# Crear una instancia de SQLAlchemy
db = SQLAlchemy()

# Definir el modelo de Nodo
class NodoModel(db.Model):
    """Modelo de la tabla nodos en la base de datos"""
    __tablename__ = 'nodos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo_cargo = db.Column(db.String(50), nullable=False) # 'directo' o 'asesoria'
    padre_id = db.Column(db.Integer, db.ForeignKey('nodo.id'))

    # Relacion recursiva para representar la jerarquia
    hijos = db.relationship('NodoModel', backref=db.backref('padre', remote_side=[id]))

    def __repr__(self):
        return f"NodoModel(id={self.id}, nombre={self.nombre}, tipo_cargo={self.tipo_cargo})"

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all() # crea si no existen las tablas
