from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from domain.services import NodoService, OrganigramaService

nodo_bp = Blueprint('nodo', __name__)

# Inicialización de servicios
nodo_service = NodoService()
organigrama_service = OrganigramaService()

@nodo_bp.route('/nodos/<int:organigrama_id>', methods=['GET'])
@jwt_required()
def obtener_nodos(organigrama_id):
    """Obtiene todos los nodos de un organigrama"""
    user_id = get_jwt_identity()

    # Verificar que el organigrama pertenece al usuario autenticado
    organigrama = organigrama_service.obtener_organigrama_por_id(organigrama_id, user_id)
    if not organigrama:
        return jsonify({"error": "Organigrama no encontrado o no autorizado"}), 404

    nodos = nodo_service.obtener_nodos_por_organigrama(organigrama_id)
    return jsonify([nodo.to_dict() for nodo in nodos]), 200

@nodo_bp.route('/nodo/<int:id>', methods=['GET'])
def obtener_nodo(id):
    """Obtiene un nodo por su ID"""
    nodo = nodo_service.obtener_nodo_por_id(id)
    if nodo:
        return jsonify(nodo.to_dict()), 200
    return jsonify({"error": "Nodo no encontrado"}), 404

@nodo_bp.route('/nodo', methods=['POST'])
@jwt_required()
def agregar_nodo():
    """Agrega un nuevo nodo a un organigrama"""
    data = request.get_json()
    user_id = get_jwt_identity()

    # Verificar que el organigrama pertenece al usuario autenticado
    organigrama_id = data.get("organigrama_id")
    organigrama = organigrama_service.obtener_organigrama_por_id(organigrama_id, user_id)
    if not organigrama:
        return jsonify({"error": "Organigrama no encontrado o no autorizado"}), 404

    try:
        nuevo_nodo = nodo_service.agregar_nodo(data)
        return jsonify(nuevo_nodo.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@nodo_bp.route('/nodo/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_nodo(id):
    """Actualiza un nodo existente"""
    data = request.get_json()
    user_id = get_jwt_identity()

    # Verificar que el nodo pertenece a un organigrama del usuario autenticado
    nodo = nodo_service.obtener_nodo_por_id(id)
    if not nodo or not organigrama_service.obtener_organigrama_por_id(nodo.organigrama_id, user_id):
        return jsonify({"error": "Nodo no encontrado o no autorizado"}), 404

    nodo_actualizado = nodo_service.actualizar_nodo(id, data)
    return jsonify(nodo_actualizado.to_dict()), 200

@nodo_bp.route('/nodo/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_nodo(id):
    """Elimina un nodo por su ID"""
    user_id = get_jwt_identity()

    # Verificar que el nodo pertenece a un organigrama del usuario autenticado
    nodo = nodo_service.obtener_nodo_por_id(id)
    if not nodo or not organigrama_service.obtener_organigrama_por_id(nodo.organigrama_id, user_id):
        return jsonify({"error": "Nodo no encontrado o no autorizado"}), 404

    eliminado = nodo_service.eliminar_nodo(id)
    if eliminado:
        return jsonify({"message": "Nodo eliminado"}), 200
    return jsonify({"error": "Error al eliminar el nodo"}), 400
