import unittest
from domain.services import OrganigramaService
from infrastructure.repositories import NodoRepository
from domain.models import Nodo

class TestOrganigramaService(unittest.TestCase):
    def setUp(self):
        self.repo = NodoRepository()
        self.service = OrganigramaService(self.repo)

    def test_agregar_nodo(self):
        """Prueba de agregacion de nodo"""
        data = {"nombre": "CEO", "tipo_cargo": "directo"}
        nodo = self.service.agregar_nodo(data)
        self.assertEqual(nodo.nombre, "CEO")
        self.assertEqual(nodo.tipo_cargo, "directo")

    def test_obtener_nodos(self):
        """Prueba de la funcion para obtener todos los nodos"""
        nodos = self.service.obtener_nodos()
        self.assertIsInstance(nodos, list)

    def test_eliminar_nodo(self):
        """Prueba de la funcion eliminar_nodo"""
        data = {"nombre": "CTO", "tipo_cargo": "directo"}
        nodo = self.service.agregar_nodo(data)
        resultado = self.service.eliminar_nodo(nodo.id)
        self.assertTrue(resultado)

if __name__ == '__main__':
    unittest.main()