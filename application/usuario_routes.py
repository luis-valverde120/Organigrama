from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from domain.services import UsuarioService

usuario_bp = Blueprint('usuario', __name__)

# Inicialización del servicio
usuario_service = UsuarioService()

@usuario_bp.route('/register', methods=['POST'])
def registrar_usuario():
    """Registra un nuevo usuario"""
    data = request.get_json()

    if not data.get('username') or not data.get('correo') or not data.get('password'):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    usuario = usuario_service.registrar_usuario(data)
    if usuario:
        return jsonify(usuario.to_dict()), 201
    return jsonify({"error": "El usuario ya existe"}), 400

@usuario_bp.route('/login', methods=['POST'])
def login():
    """Inicia sesión y devuelve un token JWT"""
    data = request.get_json()

    if not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username y contraseña son requeridos"}), 400

    tokens = usuario_service.validar_credenciales(data['username'], data['password'])

    if tokens:
        return jsonify(tokens), 200  # Asegúrate de devolver un JSON válido
    return jsonify({"error": "Credenciales incorrectas"}), 401

@usuario_bp.route('/perfil', methods=['GET'])
@jwt_required()
def obtener_perfil():
    """Obtiene el perfil del usuario autenticado"""
    user_id = get_jwt_identity()
    
    usuario = usuario_service.obtener_usuario_por_id(user_id)
    if usuario:
        return jsonify(usuario.to_dict()), 200
    return jsonify({"error": "Usuario no encontrado"}), 404
