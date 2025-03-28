from typing import Optional
from sqlalchemy.orm import Session
from domain.models import Usuario 
from infrastructure.database import db, UsuarioModel
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt

class UsuarioRepository:
    """Repositorio para manejar en la base de dato."""
     
    def __init__(self, session: Session = None):
        """
        Inicializa el repositorio.
        
        :param session: Sesion de SQLAlchemy (opcional).
        """
        self.session = session or db.session

    def crear_usuario(self, data: dict) -> Usuario:
        """
        registra un nuevo usuario en la base de datos.
        
        :param data: Datos del usuario (nombre, correo, password).
        :return: Usuario creado
        """
        try:
            password = str(data["password"])
            data["password"] = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            usuario = UsuarioModel(
                nombre=data["nombre"],
                username=data["username"],
                correo=data["correo"],
                password=data["password"],
            )
            self.session.add(usuario)
            self.session.commit()
                
            return Usuario(usuario.id, usuario.nombre, usuario.username, usuario.correo, usuario.password)
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"Error al crear usuario: {str(e)}")
    
    def obtener_usuario_por_username(self, username: str) -> Optional[Usuario]:
        """
        Obtener un usuario por username
        
        :param username: Nombre de usuario
        :return: Usuario si existe, None si no encuentra
        """
        usuario = self.session.query(UsuarioModel).filter_by(username=username).first()
        if usuario:
            return Usuario(usuario.id, usuario.nombre, usuario.username, usuario.correo, usuario.password)
        return None  # Devolver None si no se encuentra ningún usuario
    
    def obtener_usuario_por_correo(self, correo: str) -> Optional[Usuario]: 
        """
        Obtener un usuario por correo
        
        :param correo: Correo del usuario
        :return: Usuario si existe, None si no encuentra
        """
        usuario = self.session.query(UsuarioModel).filter_by(correo=correo).first()
        if usuario:
            return Usuario(usuario.id, usuario.nombre, usuario.username, usuario.correo, usuario.password)
        return None  # Devolver None si no se encuentra ningún usuario
        
    def obtener_usuario_por_id(self, id: int) -> Optional[Usuario]:
        """
        Obtener un usuario por ID
        
        :param id: Identificador del usuario
        :return: Usuario si existe, None si no encuentra
        """
        usuario = self.session.get(UsuarioModel, id)
        return Usuario(usuario.id, usuario.nombre, usuario.username, usuario.correo, usuario.password)

    def verificar_credenciales(self, username: str, password: str) -> Optional[Usuario]:
        """
        Verifica las credenciales del usuario.
        
        :param username: Nombre de usuario.
        :param password: Contraseña.
        :return: Usuario si las credenciales son validas, None en caso contrario.
        """
        usuario_db = self.session.query(UsuarioModel).filter_by(username=username).first()
        if usuario_db and check_password_hash(usuario_db.password, password):
            return Usuario(usuario_db.id, usuario_db.nombre, usuario_db.username, usuario_db.correo, usuario_db.password)
        return None