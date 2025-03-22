import unittest
from unittest.mock import MagicMock
from domain.services.nodo_service import NodoService
from domain.models import Nodo

class TestNodoService(unittest.TestCase):
    """test de la clase NodoService"""
    def setUp(self):
        """
        Configura el entorno de prueba.
        Crea un repositorio simulado y una instancia del servicio.
        """

        self.mock_repo = MagicMock()
        self.nodo_service = NodoService(nodo_repo=self.mock_repo)

    def test_agregar_nodo(self):
        """
        Prueba la función agregar_nodo.
        Verifica que se pueda agregar un nuevo nodo y que se llame al método correcto del repositorio. 
        """

        mock_repo = MagicMock()
        data = {"nombre": "Nodo 1", "titulo": "Manager", "tipo_cargo": "Gerente", "padre_id": None}
        self.mock_repo.agregar_nodo.return_value = Nodo(1, "Nodo 1", "Manager", "Gerente", mock_repo, None)

        nodo = self.nodo_service.agregar_nodo(data)

        self.assertIsNotNone(nodo)
        self.assertEqual(nodo.nombre, "Nodo 1")
        self.mock_repo.agregar_nodo.assert_called_once_with(data)

    def test_obtener_nodos(self):
        """
        Prueba la función obtener_nodos.
        Verifica que se puedan obtener todos los nodos y que se llame al método correcto del repositorio.
        """
        self.mock_repo.obtener_nodos.return_value = [Nodo(1, "Nodo 1", "Manager", "Gerente", None)]

        nodos = self.nodo_service.obtener_nodos()

        self.assertEqual(len(nodos), 1)
        self.assertEqual(nodos[0].nombre, "Nodo 1")

    def test_eliminar_nodo(self):
        """
        Prueba la función eliminar_nodo.
        Verifica que se pueda eliminar un nodo y que se llame al método correcto del repositorio.
        """
        self.mock_repo.eliminar_nodo.return_value = True

        result = self.nodo_service.eliminar_nodo(1)

        self.assertTrue(result)
        self.mock_repo.eliminar_nodo.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()
