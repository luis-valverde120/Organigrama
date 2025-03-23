from flask import Blueprint, request, jsonify
from domain.services import OrganigramaService
from flask_jwt_extended import jwt_required, get_jwt_identity

organigrama_bp = Blueprint('organigrama', __name__)

# Inicialización del servicio
organigrama_service = OrganigramaService()

@organigrama_bp.route('/organigramas', methods=['GET'])
@jwt_required()
def obtener_organigramas():
    """Obtiene todos los organigramas"""
    user_id = get_jwt_identity()
    organigramas = organigrama_service.obtener_organigramas(user_id)
    return jsonify([organigrama.to_dict() for organigrama in organigramas]), 200

@organigrama_bp.route('/organigrama/<int:id>', methods=['GET'])
@jwt_required()
def obtener_organigrama(id):
    """Obtiene un organigrama por su ID"""
    user_id = get_jwt_identity()
    organigrama = organigrama_service.obtener_organigrama_por_id(id, user_id)
    if organigrama:
        return jsonify(organigrama.to_dict()), 200
    return jsonify({"error": "Organigrama no encontrado"}), 404

@organigrama_bp.route('/organigrama', methods=['POST'])
@jwt_required()
def agregar_organigrama():
    """Agrega un nuevo organigrama"""
    data = request.get_json()
    user_id = get_jwt_identity()
    data["usuario_id"] = user_id  # Asigna el ID del usuario autenticado
    nuevo_organigrama = organigrama_service.agregar_organigrama(data)
    return jsonify(nuevo_organigrama.to_dict()), 201

@organigrama_bp.route('/organigrama/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_organigrama(id):
    """Actualiza un organigrama existente"""
    data = request.get_json()
    user_id = get_jwt_identity()
    organigrama = organigrama_service.actualizar_organigrama(id, data, user_id)
    if organigrama:
        return jsonify(organigrama.to_dict()), 200
    return jsonify({"error": "Organigrama no encontrado"}), 404

@organigrama_bp.route('/organigrama/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_organigrama(id):
    """Elimina un organigrama por su ID"""
    user_id = get_jwt_identity()
    eliminado = organigrama_service.eliminar_organigrama(id, user_id)
    if eliminado:
        return jsonify({"message": "Organigrama eliminado"}), 200
    return jsonify({"error": "Organigrama no encontrado"}), 404
