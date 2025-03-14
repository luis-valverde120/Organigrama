import unittest
from domain.services import OrganigramaService
from infrastructure.repositories import NodoRepository
from domain.models import Nodo
from infrastructure.database import db, init_db
from flask import Flask

class TestDatabaseConnection(unittest.TestCase):
    def setUp(self):
        """Configura el entorno de prueba."""
        # Crear una aplicación Flask para pruebas
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Base de datos en memoria
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Inicializar la base de datos
        init_db(self.app)

        # Crear un contexto de aplicación
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Crear las tablas en la base de datos
        db.create_all()

        # Configurar el servicio y el repositorio
        self.repo = NodoRepository()
        self.service = OrganigramaService(self.repo)

    def tearDown(self):
        """Limpia el entorno de prueba."""
        # Eliminar las tablas y cerrar la sesión
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_table(self):
        """Prueba de las tablas se crean correctamente"""
        with self.app.app_context():
            # Verificar que la tabla nodos existe
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            self.assertIn('nodos', tables)

    def test_agregar_nodo(self):
        """Prueba que se puede agreagar un nodo a la base de datos"""
        with self.app.app_context():
            # Datos del nodo
            data = {"nombre": "CEO", "tipo_cargo": "directo"}

            # Agregar el nodo
            nodo = self.service.agregar_nodo(data)

            # Verificar que el nodo se haya agregado correctamente
            self.assertIsNotNone(nodo)
            self.assertEqual(nodo.nombre, "CEO")
            self.assertEqual(nodo.tipo_cargo, "directo")

    def test_obtener_nodos(self):
        """Prueba la función obtener_nodos."""
        # Insertar un nodo de prueba
        self.repo.agregar_nodo({"nombre": "CEO", "tipo_cargo": "directo"})

        # Obtener todos los nodos
        nodos = self.service.obtener_nodos()
        self.assertEqual(len(nodos), 1)  # Verifica que haya un nodo
        self.assertEqual(nodos[0].nombre, "CEO")  # Verifica el nombre del nodo

    def test_optener_nodo_por_id(self):
        """Prueba que se puede obtener un nodo por su ID"""
        with self.app.app_context():
            # Agregar un nodo de prueba
            nodo_agregado = self.service.agregar_nodo({"nombre": "CTO", "tipo_cargo": "directo"})

            # Obtener el nodo por su ID
            nodo_obtenido = self.service.obtener_nodo_por_id(nodo_agregado.id)

            # Verificar que el nodo obtenido sea correcto
            self.assertIsNotNone(nodo_obtenido)  # Verifica que el nodo no sea None
            self.assertEqual(nodo_obtenido.nombre, "CTO")  # Verifica el nombre del nodo
            self.assertEqual(nodo_obtenido.tipo_cargo, "directo")  # Verifica el tipo de cargo

    def test_eliminar_nodo(self):
        """Prueba que se puede eliminar un nodo de la base de datos."""
        with self.app.app_context():
            # Agregar un nodo de prueba
            nodo_agregado = self.service.agregar_nodo({"nombre": "CFO", "tipo_cargo": "directo"})

            # Eliminar el nodo
            resultado = self.service.eliminar_nodo(nodo_agregado.id)

            # Verificar que el nodo se haya eliminado correctamente
            self.assertTrue(resultado)  # Verifica que la eliminación fue exitosa

            # Intentar obtener el nodo eliminado
            nodo_eliminado = self.service.obtener_nodo_por_id(nodo_agregado.id)
            self.assertIsNone(nodo_eliminado)  # Verifica que el nodo ya no exista


if __name__ == '__main__':
    unittest.main()