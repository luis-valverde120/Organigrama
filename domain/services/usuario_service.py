from flask_jwt_extended import create_access_token, create_refresh_token 
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
        return self.repo.crear_usuario(data)

    def validar_credenciales(self, username: str, password: str) -> dict:
        """
        Valida las credenciales del usuario.

        :param username: Nombre de usuario.
        :param password: Contraseña.
        :return: Diccionario con tokens si las credenciales son válidas, None en caso contrario.
        """
        user = self.repo.verificar_credenciales(username, password)

        if not user:  # <-- Posible problema aquí
            return None  # Devuelve None si las credenciales no son válidas

        try:
            access_token = create_access_token(identity=str(user.id))  # Asegúrate de que user.id sea serializable
            refresh_token = create_refresh_token(identity=str(user.id))
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
        except Exception as e:
            print(f"Error al generar tokens: {e}")
            return None

    def obtener_usuario_por_id(self, id: int) -> Usuario:
        """
        Obtiene un usuario por ID.

        :param id: Identificador del usuario.
        :return: Usuario si existe, None si no se encuentra.
        """
        return self.repo.obtener_usuario_por_id(id)

    def obtener_usuario_por_username(self, username: str) -> Usuario:
        """
        Obtiene un usuario por nombre de usuario.

        :param username: Nombre de usuario.
        :return: Usuario si existe, None si no se encuentra.
        """
        return self.repo.obtener_usuario_por_username(username)