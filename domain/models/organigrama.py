from typing import Optional, List
from domain.models.nodo import Nodo

class Organigrama:
    """Representa un organigrama que contiene nodos jerárquicos"""

    def __init__(self, id: int, nombre: str, descripcion: str, usuario_id: Optional[int] = None):
        """
        Inicializa un organigrama con un identificador y un nombre. 

        :param id: Identificador único del organigrama.
        :param nombre: Nombre del organigrama.
        :param descripcion: Descripción del organigrama.
        """
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.usuario_id: Optional[int] = usuario_id # ID del usuario propietario del organigrama.
        self.nodos: List['Nodo'] = []  # Lista de nodos en el organigrama.

    def agregar_nodo(self, nodo: Nodo):
        """
        Agrega un nodo al organigrama.

        :param nodo: Nodo a agregar al organigrama.
        """
        self.nodos.append(nodo)

    def eliminar_nodos(self, nodo_id: int):
        """
        Elimina todos los nodos del organigrama y sus decendientes.
        """
        self.nodos = [nodo for nodo in self.nodos if nodo.id != nodo_id]

    def eliminar_todos_nodos(self):
        """
        Elimina todos los nodos del organigrama.
        """
        self.nodos = []

    def to_dict(self):
        """
        Convierte el objeto Organigrama a un diccionario.

        :return: Diccionario con los atributos del organigrama.
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'usuario_id': self.usuario_id,
            'nodos': [nodo.to_dict() for nodo in self.nodos]
        }

    def __repr__(self):
        """
        Representación en cadena del organigrama para depuración.
        """ 
        return f"Organigrama(id={self.id}, nombre='{self.nombre}', descripcion='{self.descripcion}', usuario_id={self.usuario_id}, nodos={self.nodos})"
