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
                "usuario_id": data["usuario_id"],
            }

            # Descomponer el diccionario en argumentos de palabra clave
            nuevo_organigrama = OrganigramaModel(**organigrama_data)
            self.session.add(nuevo_organigrama)
            self.session.commit()
            return Organigrama(
                nuevo_organigrama.id,
                nuevo_organigrama.nombre,
            )
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"Error al agregar organigrama: {str(e)}")

    def obtener_organigramas(self, user_id: int) -> List[Organigrama]:
        """
        Obtiene todos los organigramas de un usuario.

        :param user_id: ID del usuario.
        :return: Lista de organigramas.
        """
        organigramas = self.session.query(OrganigramaModel).filter_by(usuario_id=user_id).all()
        return [Organigrama(o.id, o.nombre, o.usuario_id, o.nodos) for o in organigramas]

    def obtener_organigrama_por_id(self, id: int, user_id: int) -> Optional[Organigrama]:
        """
        Obtener un organigrama por ID y user_id.

        :param id: Identificador del organigrama.
        :param user_id: ID del usuario propietario del organigrama.
        :return: Organigrama si existe y pertenece al usuario, None si no se encuentra.
        """
        organigrama = self.session.query(OrganigramaModel).filter_by(id=id, usuario_id=user_id).first()
        if not organigrama:
            return None  # Devuelve None si no se encuentra el organigrama
        return Organigrama(organigrama.id, organigrama.nombre, organigrama.usuario_id, organigrama.nodos)

    def eliminar_organigrama(self, id: int, user_id: int) -> bool:
        """
        Elimina un organigrama de la base de datos.

        :param id: Identificador del organigrama
        :return: True si el organigrama fue eliminado, False si no se encuentra el organigrama
        """
        try:
            organigrama = self.session.query(OrganigramaModel).filter_by(id=id, usuario_id=user_id).first()
            if not organigrama:
                return False

            self.session.delete(organigrama)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"Error al eliminar organigrama: {str(e)}")

    def actualizar_organigrama(self, id: int, data: dict, user_id: int) -> Optional[Organigrama]:
        """
        Actualiza un organigrama en la base de datos.

        :param id: Identificador del organigrama.
        :param data: Datos actualizados del organigrama.
        :return: Organigrama actualizado si existe, None si no se encuentra.
        """
        try:
            organigrama = self.session.query(OrganigramaModel).filter_by(id=id, usuario_id=user_id).first()
            if not organigrama:
                return None

            for key, value in data.items():
                if hasattr(organigrama, key):
                    setattr(organigrama, key, value)

            self.session.commit()
            return Organigrama(organigrama.id, organigrama.nombre, organigrama.usuario_id)
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"Error al actualizar organigrama: {str(e)}")
