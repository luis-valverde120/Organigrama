from domain.models import Organigrama
from infrastructure.repositories import OrganigramaRepository

class OrganigramaService:
    """Servicio para manejar organigramas"""

    def __init__(self, organigrama_repo: OrganigramaRepository = None):
        """
        Inicializa el servicio de organigrama.

        :param organigrama_repo: Repositorio de organigramas (opcional).
        """
        self.organigrama_repo = organigrama_repo or OrganigramaRepository()

    def agregar_organigrama(self, data: dict) -> Organigrama:
        """
        Agrega un nuevo organigrama.

        :param data: Datos del organigrama (nombre, descripcion, etc.).
        :return: Organigrama creado.
        """
        return self.organigrama_repo.agregar_organigrama(data)

    def obtener_organigramas(self, user_id: int) -> list[Organigrama]:
        """
        Obtiene todos los organigramas de un usuario.

        :param user_id: ID del usuario.
        :return: Lista de organigramas.
        """
        return self.organigrama_repo.obtener_organigramas(user_id)

    def obtener_organigrama_por_id(self, id: int, user_id: int) -> Organigrama:
        """
        Obtiene un organigrama por su ID.

        :param id: Identificador del organigrama.
        :return: Organigrama si existe, None si no se encuentra.
        """
        return self.organigrama_repo.obtener_organigrama_por_id(id, user_id)

    def eliminar_organigrama(self, id: int, user_id: int) -> bool:
        """
        Elimina un organigrama por su ID.

        :param id: Identificador del organigrama.
        :return: True si se eliminó correctamente, False si no se encuentra.
        """
        return self.organigrama_repo.eliminar_organigrama(id, user_id)

    def actualizar_organigrama(self, id: int, data: dict, user_id: int) -> Organigrama:
        """
        Actualiza un organigrama existente.

        :param id: Identificador del organigrama.
        :param data: Datos actualizados del organigrama.
        :return: Organigrama actualizado si existe, None si no se encuentra.
        """
        return self.organigrama_repo.actualizar_organigrama(id, data, user_id)
