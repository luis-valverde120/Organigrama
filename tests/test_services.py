import unittest
from unittest.mock import MagicMock
from flask import Flask
from domain.services import OrganigramaService
from infrastructure.repositories import NodoRepository
from infrastructure.database import db, init_db
from domain.models import Nodo
from app import create_app, db

class TestOrganigramaService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()        
        self.service = OrganigramaService(self.mock_repo)

    def test_agregar_nodo(self):
        """Prueba de agregacion de nodo"""
        data = {"nombre": "Nodo 1"}

        # Simular que el repositoirio devuelve un nodo creado
        mock_nodo = {"id": 1, "nombre": "Nodo 1"}
        self.mock_repo.agregar_nodo.return_value = mock_nodo

        nodo = self.service.agregar_nodo(data)

        # Verificar que se llamo al metodo con los datos correctos
        self.mock_repo.agregar_nodo.assert_called_once_with(data)

        # Verifcar que el nodo retornado es el esperado
        self.assertEqual(nodo, mock_nodo)

    def test_obtener_nodos(self):
        """Prueba para ooptener todos los nodos"""

        # Simular que el respositorio devuelve varios nodos
        mock_nodos = [
            {"id": 1, "nombre": "Nodo 1"}, 
            {"id": 2, "nombre": "Nodo 2"},
            {"id": 3, "nombre": "Nodo 3"}
            ]
        self.mock_repo.obtener_nodos.return_value = mock_nodos

        nodos = self.service.obtener_nodos()

        # Verificar que se llamo al metodo
        self.mock_repo.obtener_nodos.assert_called_once()

        self.assertEqual(nodos, mock_nodos)

    def test_obtener_nodo_por_id(self):
        """Prueba para obtener un nodo por su id"""

        # Simular que el repositorio tiene nodos
        mock_nodo = {"id": 1, "nombre": "Nodo A"}
        self.mock_repo.obtener_nodo_por_id.return_value = mock_nodo

        # Llamar al servicio
        nodo = self.service.obtener_nodo_por_id(1)

        # Verificar que se llamo al metodo con el ID correcto
        self.mock_repo.obtener_nodo_por_id.assert_called_once_with(1)

        # Verificar que la salida es la esperada
        self.assertEqual(nodo, mock_nodo)

    def test_eliminar_nodo(self):
        """Prueba eliminar_nodo con mock"""

        # Simular que la operacion fue exitosa
        self.mock_repo.eliminar_nodo.return_value = True

        # Llamar al metodo del servicio
        resultado = self.service.eliminar_nodo(1)
        
        # Verificar que se llamo al metodo correcto con el ID
        self.mock_repo.eliminar_nodo.assert_called_once_with(1)

        # Verificar la salida esperada (True = Existo)
        self.assertTrue(resultado)

if __name__ == '__main__':
    unittest.main()