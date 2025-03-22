import unittest
from unittest.mock import MagicMock
from domain.services.organigrama_service import OrganigramaService
from domain.models import Organigrama

class TestOrganigramaService(unittest.TestCase):
    """Test de la clase OrganigramaService."""

    def setUp(self):
        """
        Configura el entorno de prueba.
        Crea un repositorio simulado y una instancia del servicio.
        """

        self.mock_organigrama_repo = MagicMock()
        self.mock_nodo_repo = MagicMock()
        self.organigrama_service = OrganigramaService(
            organigrama_repo=self.mock_organigrama_repo,
            nodo_repo=self.mock_nodo_repo
        )

    def test_agregar_organigrama(self):
        """
        Prueba la función agregar_organigrama.
        Verifica que se pueda agregar un nuevo organigrama y que se llame al método correcto del repositorio.
        """

        data = {"id": 1, "nombre": "Organigrama 1", "descripcion": "Descripción", "usuario_id": 1}
        self.mock_organigrama_repo.guardar.return_value = Organigrama(id=1, nombre="Organigrama 1", descripcion="Descripción", usuario_id=1)

        organigrama = self.organigrama_service.agregar_organigrama(data)

        self.assertIsNotNone(organigrama)
        self.assertEqual(organigrama.nombre, "Organigrama 1")
        self.mock_organigrama_repo.guardar.assert_called_once()

    def test_eliminar_organigrama(self):
        """
        Prueba la función eliminar_organigrama.
        Verifica que se pueda eliminar un organigrama y que se llame al método correcto del repositorio.
        """
        self.mock_organigrama_repo.obtener_organigrama_por_id.return_value = Organigrama(1, "Organigrama 1", "Descripción")
        self.mock_nodo_repo.eliminar_nodos_por_organigrama.return_value = True
        self.mock_organigrama_repo.eliminar.return_value = True

        result = self.organigrama_service.eliminar_organigrama(1)

        self.assertTrue(result)
        self.mock_organigrama_repo.eliminar.assert_called_once()

    def test_actualizar_nombre_organigrama(self):
        """
        Prueba la función actualizar_nombre_organigrama.
        Verifica que se pueda actualizar el nombre de un organigrama y que se llame al método correcto del repositorio.
        """

        self.mock_organigrama_repo.actualizar_nombre.return_value = Organigrama(1, "Nuevo Nombre", "Descripción")

        organigrama = self.organigrama_service.actualizar_nombre_organigrama(1, "Nuevo Nombre")

        self.assertIsNotNone(organigrama)
        self.assertEqual(organigrama.nombre, "Nuevo Nombre")
        self.mock_organigrama_repo.actualizar_nombre.assert_called_once_with(1, "Nuevo Nombre")

if __name__ == "__main__":
    unittest.main()
