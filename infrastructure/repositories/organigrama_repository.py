from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models import Organigrama
from infrastructure.database import db, OrganigramaModel

class OrganigramaRepository:
    """Repositorio para interactuar con la base de datos de organigramas"""

    def __init__(self, session: Session = None):
        """
        Inicializa el repositorio.

        :param session: Sesion de SQLAlchemy (opcional).
        """
        self.session = session or db.session

    def agregar_organigrama(self, data: dict) -> Organigrama:
        """
        Agrega un nuevo organigrama a la base de datos.

        :param data: Datos del organigrama (nombre, descripcion, etc.).
        :return: Organigrama creado
        """
        try:
            organigrama_data = {
                "nombre": data["nombre"],
                "descripcion": data["descripcion"],
            }

            nuevo_organigrama = OrganigramaModel(**organigrama_data)
            self.session.add(nuevo_organigrama)
            self.session.commit()
            return Organigrama(
                nuevo_organigrama.id,
                nuevo_organigrama.nombre,
                nuevo_organigrama.descripcion,
            )
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"Error al agregar organigrama: {str(e)}")

    def obtener_organigramas(self) -> List[Organigrama]:
        """
        Obtiene todos los organigramas de la base de datos

        :return: Lista de organigramas.
        """
        organigrama = self.session.query(OrganigramaModel).all()
        return [Organigrama(o.id, o.nombre, o.descripcion) for o in organigrama]

    def obtener_organigrama_por_id(self, id: int) -> Optional[Organigrama]:
        """
        Obtener un organigrama por ID

        :param id: Identificador del organigrama
        :return: Organigrama si existe, None si no encuentra
        """
        organigrama = self.session.get(OrganigramaModel, id)
        if not organigrama:
            return None
        return Organigrama(organigrama.id, organigrama.nombre, organigrama.descripcion)

    def eliminar_organigrama(self, id: int) -> bool:
        """
        Elimina un organigrama de la base de datos.

        :param id: Identificador del organigrama
        :return: True si el organigrama fue eliminado, False si no se encuentra el organigrama
        """
        try:
            organigrama = self.session.get(OrganigramaModel, id)
            if not organigrama:
                return False

            self.session.delete(organigrama)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"Error al eliminar organigrama: {str(e)}")

    def actualizar_organigrama(self, id: int, data: dict) -> Optional[Organigrama]:
        """
        Actualiza un organigrama en la base de datos.

        :param id: Identificador del organigrama.
        :param data: Datos actualizados del organigrama.
        :return: Organigrama actualizado si existe, None si no se encuentra.
        """
        try:
            organigrama = self.session.get(OrganigramaModel, id)
            if not organigrama:
                return None

            for key, value in data.items():
                if hasattr(organigrama, key):
                    setattr(organigrama, key, value)

            self.session.commit()
            return Organigrama(organigrama.id, organigrama.nombre, organigrama.descripcion)
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"Error al actualizar organigrama: {str(e)}")
