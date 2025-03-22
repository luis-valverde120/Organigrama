from flask import Blueprint, request, jsonify
from domain.services import OrganigramaService

organigrama_bp = Blueprint('organigrama', __name__)

# Inicialización del servicio
organigrama_service = OrganigramaService()

@organigrama_bp.route('/organigramas', methods=['GET'])
def obtener_organigramas():
    """Obtiene todos los organigramas"""
    organigramas = organigrama_service.obtener_organigramas()
    return jsonify([organigrama.to_dict() for organigrama in organigramas]), 200

@organigrama_bp.route('/organigrama/<int:id>', methods=['GET'])
def obtener_organigrama(id):
    """Obtiene un organigrama por su ID"""
    organigrama = organigrama_service.obtener_organigrama_por_id(id)
    if organigrama:
        return jsonify(organigrama.to_dict()), 200
    return jsonify({"error": "Organigrama no encontrado"}), 404

@organigrama_bp.route('/organigrama', methods=['POST'])
def agregar_organigrama():
    """Agrega un nuevo organigrama"""
    data = request.get_json()
    nuevo_organigrama = organigrama_service.agregar_organigrama(data)
    return jsonify(nuevo_organigrama.to_dict()), 201

@organigrama_bp.route('/organigrama/<int:id>', methods=['PUT'])
def actualizar_organigrama(id):
    """Actualiza un organigrama existente"""
    data = request.get_json()
    organigrama = organigrama_service.actualizar_organigrama(id, data)
    if organigrama:
        return jsonify(organigrama.to_dict()), 200
    return jsonify({"error": "Organigrama no encontrado"}), 404

@organigrama_bp.route('/organigrama/<int:id>', methods=['DELETE'])
def eliminar_organigrama(id):
    """Elimina un organigrama por su ID"""
    eliminado = organigrama_service.eliminar_organigrama(id)
    if eliminado:
        return jsonify({"message": "Organigrama eliminado"}), 200
    return jsonify({"error": "Organigrama no encontrado"}), 404
