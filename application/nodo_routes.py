from flask import Blueprint, request, jsonify
from domain.services import NodoService

nodo_bp = Blueprint('nodo', __name__)

# Inicialización del servicio
nodo_service = NodoService()

@nodo_bp.route('/nodos', methods=['GET'])
def obtener_nodos():
    """Obtiene todos los nodos"""
    nodos = nodo_service.obtener_nodos()
    return jsonify([nodo.to_dict() for nodo in nodos]), 200

@nodo_bp.route('/nodo/<int:id>', methods=['GET'])
def obtener_nodo(id):
    """Obtiene un nodo por su ID"""
    nodo = nodo_service.obtener_nodo_por_id(id)
    if nodo:
        return jsonify(nodo.to_dict()), 200
    return jsonify({"error": "Nodo no encontrado"}), 404

@nodo_bp.route('/nodo', methods=['POST'])
def agregar_nodo():
    """Agrega un nuevo nodo"""
    data = request.get_json()
    try:
        nuevo_nodo = nodo_service.agregar_nodo(data)
        return jsonify(nuevo_nodo.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@nodo_bp.route('/nodo/<int:id>', methods=['PUT'])
def actualizar_nodo(id):
    """Actualiza un nodo existente"""
    data = request.get_json()
    nodo = nodo_service.actualizar_nodo(id, data)
    if nodo:
        return jsonify(nodo.to_dict()), 200
    return jsonify({"error": "Nodo no encontrado"}), 404

@nodo_bp.route('/nodo/<int:id>', methods=['DELETE'])
def eliminar_nodo(id):
    """Elimina un nodo por su ID"""
    eliminado = nodo_service.eliminar_nodo(id)
    if eliminado:
        return jsonify({"message": "Nodo eliminado"}), 200
    return jsonify({"error": "Nodo no encontrado"}), 404
