from domain.models import Organigrama
from infrastructure.database import OrganigramaModel
from infrastructure.database import db
from sqlalchemy.orm import Session

class OrganigramaRepository:
    """Repositorio para interactuar con la base de datos de organigramas"""

    def __init__(self, session: Session = None):
        """
        Inicializa el repositorio.

        :param session: Sesion de SQLAlchemy (opcional).
        """
        self.session = session or db.session

    def guardar(self, data: dict) -> Organigrama:
        """
        Guarda un nuevo organigrama en la base de datos.

        :param organigrama: Organigrama a guardar.
        :return: Organigrama guardado.
        """
        nuevo_organigrama = OrganigramaModel(**data)
        self.session.add(nuevo_organigrama)
        self.session.commit()
        return Organigrama(nuevo_organigrama.id, nuevo_organigrama.nombre, nuevo_organigrama.descripcion, nuevo_organigrama.usuario_id)

    def obtener_organigramas_por_usuario(self, usuario_id: int):
        """
        Obtiene todos los organigramas de un usuario.

        :param usuario_id: ID del usuario.
        :return: Lista de organigramas.
        """
        return self.session.query(Organigrama).filter_by(usuario_id=usuario_id).all()

    def obtener_organigrama_por_id(self, organigrama_id: int) -> Organigrama:
        """
        Obtiene un organigrama por ID.

        :param organigrama_id: ID del organigrama.
        :return: Organigrama si existe, None si no se encuentra.
        """
        return self.session.query(Organigrama).get(organigrama_id)

    def eliminar(self, organigrama: Organigrama) -> bool:
        """
        Elimina un organigrama.

        :param organigrama: Organigrama a eliminar.
        :return: True si se eliminó correctamente.
        """
        self.session.delete(organigrama)
        self.session.commit()
        return True

    def actualizar_nombre(self, organigrama_id: int, nuevo_nombre: str) -> Organigrama:
        """
        Actualiza el nombre de un organigrama.

        :param organigrama_id: ID del organigrama a actualizar.
        :param nuevo_nombre: Nuevo nombre para el organigrama.
        :return: Organigrama actualizado.
        """
        organigrama = self.obtener_organigrama_por_id(organigrama_id)
        if not organigrama:
            return None
        organigrama.nombre = nuevo_nombre
        self.session.commit()
        return organigrama