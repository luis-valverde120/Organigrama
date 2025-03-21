from typing import List, Optional
from domain.models import Nodo
from infrastructure.repositories import NodoRepository

class OrganigramaService:
    """Servicio para manejar la logica de negocios del organigrama"""

    def __init__(self, repo: NodoRepository = None):
        """
        Inicializa el servicio.

        :param repo: Repositorio para interactuar con la base de datos.
        """
        self.repo = repo or NodoRepository()

    
    def agregar_nodo(self, data: dict) -> Nodo:
        """
        Agrega un nuevo nodo al organigrama.

        :param data: Datos del nodo (nombre, tipo_cargo, padre_id).
        :return Nodo creado 
        """
        return self.repo.agregar_nodo(data)
    
    def obtener_nodos(self) -> List[Nodo]:
        """
        Obtiene todos los nodos del organigrama

        :return: Lista de nodos.
        """
        return self.repo.obtener_nodos()

    def eliminar_nodo(self, id: int) -> bool:
        """
        Elimina un nodo del organigrama.

        :param id: Identificador del nodo.
        :return: True si el nodo fue eliminado, false si no se encuentra
        """
        return self.repo.eliminar_nodo(id)

    def obtener_nodo_por_id(self, id: int) -> bool:
        """
        Obtener un nodo por el ID

        :param id: Identificador del nodo.
        :return: Nodo si existe, None si no se encuentra
        """
        return self.repo.obtener_nodo_por_id(id)

    def actualizar_nodo(self, id: int, data: dict) -> Optional[Nodo]:
        """
        Actualiza un nodo del organigrama.

        :param id: Identificador del nodo.
        :param data: Datos actualizados del nodo.
        :return: Nodo actualizado si existe, None si no se encuentra.
        """
        return self.repo.actualizar_nodo(id, data)

