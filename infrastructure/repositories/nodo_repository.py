from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models import Nodo
from infrastructure.database import db, NodoModel

class NodoRepository:
    """Repositorio para interactuar con la base de datos de nodos"""

    def __init__(self, session: Session = None):
        """
        Inicializa el repositorio.

        :param session: Sesion de SQLAlchemy (opcional).
        """
        self.session = session or db.session

    def agregar_nodo(self, data: dict) -> Nodo:
        """
        Agrega un nuevo nodo a la base de datos.

        :param data: Datos del nodo (nombre, titulo, tipo_cargo, organigrama_id, padre_id).
        :return: Nodo creado
        """
        try:
            # Filtrar las claves relevantes para el modelo NodoModel
            nodo_data = {
                "nombre": data["nombre"],
                "titulo": data["titulo"],
                "tipo_cargo": data["tipo_cargo"],
                "organigrama_id": data["organigrama_id"],
                "padre_id": data.get("padre_id"),  # Puede ser opcional
            }

            organigrama = self.session.query(NodoModel).filter_by(id=data["organigrama_id"]).first()

            nuevo_nodo = NodoModel(**nodo_data)
            self.session.add(nuevo_nodo)
            self.session.commit()
            return Nodo(
                nuevo_nodo.id,
                nuevo_nodo.nombre,
                nuevo_nodo.titulo,
                nuevo_nodo.tipo_cargo,
                nuevo_nodo.organigrama_id,
                nuevo_nodo.padre_id,
            )
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"Error al agregar nodo: {str(e)}")

    def obtener_nodos(self) -> List[Nodo]:
        """
        Obtiene todos los nodos de la base de datos

        :return: Lista de nodos.
        """
        nodo = self.session.query(NodoModel).all()
        return [Nodo(n.id, n.nombre, n.titulo, n.tipo_cargo, n.organigrama_id, n.padre_id, n.color_bg, n.color_border, n.color_text) for n in nodo]

    def obtener_nodo_por_id(self, id: int) -> Optional[Nodo]:
        """
        Obtener un nodo por ID

        :param id: Identificador del nodo
        :return: Nodo si existe, None si no encuentra
        """
        nodo = self.session.get(NodoModel, id)
        if not nodo:
            return None
        return Nodo(nodo.id, nodo.nombre, nodo.titulo, nodo.tipo_cargo, nodo.organigrama_id,nodo.padre_id)

    def eliminar_nodo(self, id: int) -> bool:
        """
        Elimina un nodo de la base de datos. Si el nodo tiene hijos, también se eliminan.
        Si el nodo es un hijo, no afecta al nodo padre.

        :param id: Identificador del nodo.
        :return: True si el nodo fue eliminado, False si no se encuentra el nodo.
        """
        try:
            nodo = self.session.get(NodoModel, id)
            if not nodo:
                return False

            # Verificar si el nodo tiene hijos
            nodos_hijos = self.session.query(NodoModel).filter_by(padre_id=id).all()
            for hijo in nodos_hijos:
                self.session.delete(hijo)  # Eliminar todos los hijos del nodo

            # Eliminar el nodo actual
            self.session.delete(nodo)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"Error al eliminar nodo: {str(e)}")

    def actualizar_nodo(self, id: int, data: dict) -> Optional[Nodo]:
        """
        Actualiza un nodo en la base de datos.

        :param id: Identificador del nodo.
        :param data: Datos actualizados del nodo.
        :return: Nodo actualizado si existe, None si no se encuentra.
        """
        try:
            nodo = self.session.get(NodoModel, id)
            if not nodo:
                return None

            # Actualizar los campos del nodo, incluyendo los colores
            for key, value in data.items():
                if hasattr(nodo, key):
                    setattr(nodo, key, value)

            self.session.commit()
            return Nodo(
                nodo.id,
                nodo.nombre,
                nodo.titulo,
                nodo.tipo_cargo,
                nodo.organigrama_id,
                nodo.padre_id,
                nodo.color_bg,
                nodo.color_border,
                nodo.color_text
            )
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"Error al actualizar nodo: {str(e)}")

    def eliminar_nodos_descendientes(self, nodo_id: int):
        """
        Elimina todos los nodos descendientes de un nodo específico.

        :param nodo_id: ID del nodo padre cuyos descendientes serán eliminados.
        """
        nodos_hijos = self.session.query(NodoModel).filter(NodoModel.padre_id == nodo_id).all()
        for nodo_hijo in nodos_hijos:
            # Llamada recursiva para eliminar los descendientes del nodo hijo
            self.eliminar_nodos_descendientes(nodo_hijo.id)
            self.session.delete(nodo_hijo)
        self.session.commit()

    def obtener_nodos_por_organigrama(self, organigrama_id: int) -> List[Nodo]:
        """
        Obtiene todos los nodos de un organigrama.

        :param organigrama_id: ID del organigrama.
        :return: Lista de nodos.
        """
        nodos = self.session.query(NodoModel).filter_by(organigrama_id=organigrama_id).all()
        return [Nodo(n.id, n.nombre, n.titulo, n.tipo_cargo, n.organigrama_id, n.padre_id, n.color_bg, n.color_border, n.color_text) for n in nodos]
