import unittest
from unittest.mock import MagicMock
from domain.services.usuario_service import UsuarioService
from domain.models import Usuario
from flask import Flask
from flask_jwt_extended import JWTManager

class TestUsuarioService(unittest.TestCase):
    """
    Test de versión de la clase UsuarioService.
    """
    def setUp(self):
        """
        Configura el entorno de prueba. 
        Crea un repositorio simulado y una instancia del servicio.
        """
        # Configurar la aplicación Flask y JWT
        self.app = Flask(__name__)
        self.app.config['JWT_SECRET_KEY'] = 'test_secret_key'
        self.jwt = JWTManager(self.app)

        self.mock_repo = MagicMock()
        self.usuario_service = UsuarioService(repo=self.mock_repo)

    def test_registrar_usuario(self):
        """
        Prueba la función registrar_usuario.
        Verifica que se pueda registrar un nuevo usuario y que se llame al método correcto del repositorio.
        """

        data = {
            "nombre": "John Doe",
            "username": "johndoe",
            "correo": "johndoe@example.com",
            "password": "password123"
        }
        self.mock_repo.obtener_usuario_por_username.return_value = None
        self.mock_repo.obtener_usuario_por_correo.return_value = None
        self.mock_repo.crear_usaurio.return_value = Usuario(1, "John Doe", "johndoe", "johndoe@example.com", "hashed_password")

        usuario = self.usuario_service.registrar_usuario(data)

        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.nombre, "John Doe")
        self.mock_repo.crear_usaurio.assert_called_once()

    def test_validar_credenciales(self):
        """
        Prueba la función validar_credenciales.
        Verifica que se pueda validar las credenciales de un usuario y que se genere un token.
        """
        with self.app.app_context():  # Contexto de aplicación
            self.mock_repo.verificar_credenciales.return_value = Usuario(
                1, "John Doe", "johndoe", "johndoe@example.com", "hashed_password"
            )

            result = self.usuario_service.validar_credenciales("johndoe", "password123")

            self.assertIsNotNone(result)
            self.assertIn("access_token", result)
            self.assertIn("refresh_token", result)

    def test_obtener_usuario_por_id(self):
        """
        Prueba la función obtener_usuario_por_id.
        Verifica que se pueda obtener un usuario por su ID.
        """

        self.mock_repo.obtener_usuario_por_id.return_value = Usuario(1, "John Doe", "johndoe", "johndoe@example.com", "hashed_password")

        usuario = self.usuario_service.obtener_usuario_por_id(1)

        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.id, 1)
        self.assertEqual(usuario.nombre, "John Doe")

if __name__ == "__main__":
    unittest.main()
