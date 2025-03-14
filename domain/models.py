
class Nodo:
    """ Representa un nodo en el organigrama """
    def __init__(self, id: int, nombre: str, tipo_cargo: str, padre_id: int = None):
        """
        Inizializacion del Nodo

        :param id: Identificador del nodo unico.
        :param nombre: Nombre del nodo.
        :param tipo_cargo: Tipo de cargo {'directo' o 'asesoria'}.
        :param padre_id: Identificador del nodo padre (opcional).
        """
        self.id = id
        self.nombre = nombre
        self.tipo_cargo = tipo_cargo
        self.padre_id = padre_id

    def __repr__(self):
        return f"Nodo(id={self.id}, nombre={self.nombre}, tipo_cargo={self.tipo_cargo})"