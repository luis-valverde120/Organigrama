from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta
from domain.models import Usuario
from infrastructure.repositories.usuario_repository import UsuarioRepository

class UsuarioService:
    """Servicio para manejar usuarios y autenticación"""

    def __init__(self, repo=None):
        """
        Inicializa el servicio.

        :param repo: Repositorio para interactuar con la base de datos.
        """
        self.repo = repo or UsuarioRepository()

    def registrar_usuario(self, data: dict) -> Usuario:
        """
        Registra un nuevo usuario en la base de datos.

        :param data: Datos del usuario (nombre, username, correo, password).
        :return: Usuario creado o None si ya existe.
        """
        # Verificar si el usuario ya existe
        if self.repo.obtener_usuario_por_username(data['username']) or self.repo.obtener_usuario_por_correo(data['correo']):
            return None

        # Crear el usuario
        data['password'] = generate_password_hash(data['password'], method='pbkdf2:sha256')
        return self.repo.crear_usaurio(data)

    def validar_credenciales(self, username: str, password: str) -> dict:
        """
        Valida las credenciales del usuario.

        :param username: Nombre de usuario.
        :param password: Contraseña.
        :return: Diccionario con tokens si las credenciales son válidas, None en caso contrario.
        """
        user = self.repo.verificar_credenciales(username, password)
        if user:
            return {
                'access_token': create_access_token(identity=user.id, expires_delta=timedelta(days=1)),
                'refresh_token': create_access_token(identity=user.id),
            }
        return None

    def obtener_usuario_por_id(self, id: int) -> Usuario:
        """
        Obtiene un usuario por ID.

        :param id: Identificador del usuario.
        :return: Usuario si existe, None si no se encuentra.
        """
        return self.repo.obtener_usuario_por_id(id)