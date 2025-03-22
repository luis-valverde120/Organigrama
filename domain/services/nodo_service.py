from domain.models import Nodo
from infrastructure.repositories import NodoRepository, OrganigramaRepository

class NodoService:
    """Servicio para manejar nodos"""

    def __init__(self, nodo_repo: NodoRepository = None, organigrama_repo: OrganigramaRepository = None):
        """
        Inicializa el servicio de nodos.

        :param nodo_repo: Repositorio de nodos (opcional).
        :param organigrama_repo: Repositorio de organigramas (opcional).
        """
        self.nodo_repo = nodo_repo or NodoRepository()
        self.organigrama_repo = organigrama_repo or OrganigramaRepository()

    def agregar_nodo(self, data: dict) -> Nodo:
        """
        Agrega un nuevo nodo.

        :param data: Datos del nodo (nombre, tipo_cargo, organigrama_id, etc.).
        :return: Nodo creado.
        :raises ValueError: Si el organigrama no existe.
        """
        # Validar si el organigrama_id existe
        organigrama_id = data.get('organigrama_id')
        if not organigrama_id or not self.organigrama_repo.obtener_organigrama_por_id(organigrama_id):
            raise ValueError("El organigrama asociado no es válido o no existe.")

        return self.nodo_repo.agregar_nodo(data)

    def obtener_nodos(self) -> list[Nodo]:
        """
        Obtiene todos los nodos.

        :return: Lista de nodos.
        """
        return self.nodo_repo.obtener_nodos()

    def obtener_nodo_por_id(self, id: int) -> Nodo:
        """
        Obtiene un nodo por su ID.

        :param id: Identificador del nodo.
        :return: Nodo si existe, None si no se encuentra.
        """
        return self.nodo_repo.obtener_nodo_por_id(id)

    def eliminar_nodo(self, id: int) -> bool:
        """
        Elimina un nodo por su ID.

        :param id: Identificador del nodo.
        :return: True si se eliminó correctamente, False si no se encuentra.
        """
        return self.nodo_repo.eliminar_nodo(id)

    def actualizar_nodo(self, id: int, data: dict) -> Nodo:
        """
        Actualiza un nodo existente.

        :param id: Identificador del nodo.
        :param data: Datos actualizados del nodo.
        :return: Nodo actualizado si existe, None si no se encuentra.
        """
        return self.nodo_repo.actualizar_nodo(id, data)
