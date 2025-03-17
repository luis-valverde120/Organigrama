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

        :param data: Datos del nodo (nombre, tipo_cargo, padre_id).
        :return: Nodo creado
        """
        nuevo_nodo = NodoModel(**data)
        self.session.add(nuevo_nodo)
        self.session.commit()
        return Nodo(nuevo_nodo.id, nuevo_nodo.nombre, nuevo_nodo.titulo, nuevo_nodo.tipo_cargo , nuevo_nodo.padre_id)

    def obtener_nodos(self) -> List[Nodo]:
        """
        Obtiene todos los nodos de la base de datos

        :return: Lista de nodos.
        """
        nodos = self.session.query(NodoModel).all()
        return [Nodo(n.id, n.nombre, n.titulo, n.tipo_cargo, n.padre_id) for n in nodos]

    def obtener_nodo_por_id(self, id: int) -> Optional[Nodo]:
        """
        Obtener un nodo por ID

        :param id: Identificador del nodo
        :return: Nodo si existe, None si no encuentra
        """
        nodo = self.session.get(NodoModel, id)
        if nodo:
            return Nodo(nodo.id, nodo.nombre, nodo.titulo, nodo.tipo_cargo, nodo.padre_id)
        return None

    def eliminar_nodo(self, id: int) -> bool:
        """
        Elimina unnodo de la base de datos.

        :param id: Identificador del nodo
        :return: True si el nodo fue eliminado, False si no se encuentra el nodo
        """
        nodo = self.session.get(NodoModel, id)
        if nodo:
            self.session.delete(nodo)
            self.session.commit()
            return True
        return False
        
    def actualizar_nodo(self, id, data: dict) -> Optional[Nodo]:
        """
        Actualiza un nodo en la base de datos.

        :param id: Identificador del nodo.
        :param data: Datos actualizados del nodo.
        :return: Nodo actualizado si existe, None si no se encuentra.
        """
        nodo = self.session.get(NodoModel, id)
        if nodo:
            # Actualizar los atributos del nodo
            nodo.nombre = data.get('nombre', nodo.nombre)
            nodo.titulo = data.get('titulo', nodo.titulo)
            nodo.tipo_cargo = data.get('tipo_cargo', nodo.tipo_cargo)
            nodo.padre_id = data.get('padre_id', nodo.padre_id)
            
            self.session.commit()  # Guardar los cambios en la base de datos
            return Nodo(nodo.id, nodo.nombre, nodo.titulo, nodo.tipo_cargo, nodo.padre_id)
        return None