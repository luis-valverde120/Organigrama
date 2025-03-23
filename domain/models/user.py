import bcrypt

class Usuario:
    """Representa un usuario en el sistema"""
    def __init__(self, id: int, nombre: str, username: str, email: str, password:str):
        """
        Inicializa un usuario con un identificador, nombre y correo electrónico.

        :param id: Identificador único del usuario.
        :param nombre: Nombre del usuario.
        :param email: Correo electrónico del usuario.
        """
        self.id = id
        self.nombre = nombre
        self.username = username
        self.email = email
        self.password = self._hash_password(password) 
        self.organigramas = []

    def _hash_password(self, password: str) -> str:
        """
        Hash de la contraseña antes de guardarla
        
        :param password: Contraseña a encriptar.
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verificar_password(self, password: str) -> bool:
        """
        Verifica si la contraseña proporcionada coincide con la contraseña encriptada.

        :param password: Contraseña a verificar.
        :return: True si la contraseña es correcta, False en caso contrario.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    def obtener_organigramas(self):
        """ Obtener organigramas del usuario """
        return self.organigramas

    def agregar_organigrama(self, organigrama):
        """
        Agrega un organigrama a la lista de organigramas del usuario.

        :param organigrama: Organigrama a agregar.
        """
        self.organigramas.append(organigrama)

    def to_dict(self):
        """
        Convierte el objeto Usuario a un diccionario.

        :return: Diccionario con los atributos del usuario.
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'username': self.username,
            'email': self.email,
            'password': self.password
        }

    def __repr__(self):
        """
        Representación en cadena del usuario para depuración.
        """
        return f"Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}')"
    
    