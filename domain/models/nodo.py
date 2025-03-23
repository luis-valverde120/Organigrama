from typing import List, Optional

class Nodo:
    """ Representa un nodo en el organigrama """

    def __init__(
            self, 
            id: int, 
            nombre: str, 
            titulo: str, 
            tipo_cargo: str, 
            organigrama_id: int, 
            padre: Optional[int] = None,
            color_bg: str = "#FFFFFF",
            color_border: str = "#000000",
            color_text: str = "#000000"
            ):
        """
        Inicializa un nodo 
        :param id: Identificador único del nodo.
        :param nombre: Nombre del nodo.
        :param titulo: Título del nodo.
        :param tipo_cargo: Tipo de cargo del nodo.
        :param organigrama_id: ID del organigrama al que pertenece el nodo.
        :param padre: ID del nodo padre, si existe.
        """
        self.id = id
        self.nombre = nombre
        self.titulo = titulo
        self.tipo_cargo = tipo_cargo
        self.organigrama_id = organigrama_id  # Relación con el organigrama al que pertenece.
        self.padre: Optional[int] = padre  # ID del nodo padre.
        self.hijos: List['Nodo'] = []  # Inicializa la lista de hijos como vacía.

        # Colores para la representación visual del nodo
        self.color_bg = color_bg
        self.color_border = color_border
        self.color_text = color_text

    def agregar_hijo(self, nodo: 'Nodo'):
        """
        Agrega un nodo hijo al nodo actual.

        :param nodo: Nodo hijo a agregar.
        """
        nodo.padre = self.id  # Establece el ID del nodo actual como el padre del nuevo hijo.
        self.hijos.append(nodo)  # Agrega el nodo hijo a la lista de hijos.

    def eliminar_hijo(self, nodo_id: int):
        """
        Elimina un nodo hijo del nodo actual.

        :param nodo_id: Identificador del nodo hijo a eliminar.
        """
        for hijo in self.hijos:
            if hijo.id == nodo_id:
                hijo.eliminar_descendientes()
                self.hijos.remove(hijo)

    def eliminar_descendientes(self):
        """
        Elimina todos los nodos descendientes del nodo actual.
        """
        for hijo in self.hijos:
            hijo.eliminar_descendientes()
        self.hijos = []

    def obtener_descendientes(self) -> List['Nodo']:
        """
        Obtiene todos los nodos descendientes del nodo actual.

        :return: Lista de nodos descendientes.
        """
        descendientes = []
        for hijo in self.hijos:
            descendientes.append(hijo)
            descendientes.extend(hijo.obtener_descendientes())
        return descendientes    
    
    def to_dict(self) -> dict:
        """
        Convierte el nodo a un diccionario.

        :return: Diccionario representando el nodo.
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'titulo': self.titulo,
            'tipo_cargo': self.tipo_cargo,
            'organigrama_id': self.organigrama_id,
            'padre_id': self.padre,  # Usar directamente el ID del padre
            'hijos': [hijo.to_dict() for hijo in self.hijos],
            'color_bg': self.color_bg,
            'color_border': self.color_border,
            'color_text': self.color_text
        }

    def __repr__(self):
        """
        Representación en cadena del nodo para depuración.
        """
        return f"Nodo(id={self.id}, nombre='{self.nombre}')"