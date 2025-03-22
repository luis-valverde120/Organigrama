from domain.models import Organigrama
from infrastructure.repositories import OrganigramaRepository
from infrastructure.repositories import NodoRepository

class OrganigramaService:
    """Servicio para manejar organigramas"""

    def __init__(self, organigrama_repo: OrganigramaRepository = None, nodo_repo: NodoRepository = None):
        self.organigrama_repo = organigrama_repo or OrganigramaRepository()
        self.nodo_repo = nodo_repo or NodoRepository()

    def obtener_organigramas(self, usuario_id: int):
        """
        Obtiene todos los organigramas del usuario.
        
        :param usuario_id: ID del usuario.
        :return: Lista de organigramas.
        """
        return self.organigrama_repo.obtener_organigramas_por_usuario(usuario_id)

    def agregar_organigrama(self, data: dict) -> Organigrama:
        """
        Agrega un nuevo organigrama.
        
        :param data: Datos del organigrama.
        :return: Organigrama creado.
        """

        return self.organigrama_repo.guardar(data)

    def eliminar_organigrama(self, organigrama_id: int) -> bool:
        """
        Elimina un organigrama y sus nodos asociados.
        
        :param organigrama_id: ID del organigrama.
        :return: True si se eliminó, False en caso contrario.
        """
        organigrama = self.organigrama_repo.obtener_organigrama_por_id(organigrama_id)
        if not organigrama:
            return False
        
        # Eliminar nodos asociados al organigrama
        self.nodo_repo.eliminar_nodos_por_organigrama(organigrama_id)
        return self.organigrama_repo.eliminar(organigrama)

    def actualizar_nombre_organigrama(self, organigrama_id: int, nuevo_nombre: str) -> Organigrama:
        """
        Actualiza el nombre de un organigrama.
        
        :param organigrama_id: ID del organigrama.
        :param nuevo_nombre: Nuevo nombre para el organigrama.
        :return: Organigrama actualizado.
        """
        return self.organigrama_repo.actualizar_nombre(organigrama_id, nuevo_nombre)

    def agregar_nodo(self, data: dict):
        """
        Agrega un nodo al organigrama.
        
        :param data: Datos del nodo, incluyendo el ID del organigrama.
        :return: Nodo creado.
        :raises ValueError: Si falta el organigrama_id en los datos.
        """
        if 'organigrama_id' not in data:
            raise ValueError("El campo 'organigrama_id' es obligatorio para agregar un nodo.")
        
        # Crear el nodo usando el repositorio de nodos
        return self.nodo_repo.agregar_nodo(data)