class Nodo:
    """ Representa un nodo en el organigrama """
    def __init__(self, id: int, nombre: str, titulo: str, tipo_cargo: str, padre_id: int = None):
        """
        Inicialización del Nodo

        :param id: Identificador único del nodo.
        :param nombre: Nombre de la persona en el nodo.
        :param titulo: Cargo de la persona (ejemplo: "CEO", "Jefe", "Gerente").
        :param tipo_cargo: Tipo de cargo {'directo' o 'asesoria'}.
        :param padre_id: Identificador del nodo padre (opcional).
        """
        self.id = id
        self.nombre = nombre
        self.titulo = titulo  # Nuevo atributo para el cargo/título
        self.tipo_cargo = tipo_cargo
        self.padre_id = padre_id

    def __repr__(self):
        return f"Nodo(id={self.id}, nombre={self.nombre}, titulo={self.titulo}, tipo_cargo={self.tipo_cargo})"
