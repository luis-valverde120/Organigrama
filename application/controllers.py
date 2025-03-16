from flask import Blueprint, request, jsonify
from domain.services import OrganigramaService


# Crear un blueprint para las rutas
organigrama_blueprint = Blueprint('organigrama', __name__)
service = OrganigramaService()


@organigrama_blueprint.route('/nodos', methods=['GET'])
def get_nodos():
    """Obtiene todos los nodos del organigrama"""
    nodos = service.obtener_nodos()
    return jsonify([n.__dict__ for n in nodos])

@organigrama_blueprint.route('/nodos', methods=['POST'])
def add_nodo():
    """Agregar un nuevo nodo al organigrama"""
    data = request.json
    nodo = service.agregar_nodo(data)
    return jsonify(nodo.__dict__), 201

@organigrama_blueprint.route('/nodos/<int:id>', methods=['GET'])
def get_nodo_by_id(id):
    """Obtener nodos por id"""
    nodo = service.obtener_nodo_por_id(id)
    if nodo:
        return jsonify(nodo.__dict__)
    return jsonify({"error": "Nodo no encontrado"}), 404

@organigrama_blueprint.route('/nodos/<int:id>', methods=['DELETE'])
def delete_nodo(id):
    """Elimina un nodo del organigrama"""
    if service.eliminar_nodo(id):
        return '',204
    return jsonify({"error": "Nodo no encontrado"}), 404