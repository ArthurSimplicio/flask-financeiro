from flask import Blueprint, request, jsonify
from app.services.categoria_service import criar_categoria, listar_categorias
from app.utils.response import response

from flask_jwt_extended import jwt_required

categoria_bp = Blueprint("categoria", __name__, url_prefix="/categorias")

@categoria_bp.route("", methods=["POST"])
@jwt_required()
def create_categoria():
    try:
        data = request.get_json()
        nome = data.get("nome")
        if not nome:
            return response("error", "nome obrigatorio", 400)
        
        categoria = criar_categoria(nome=nome)
        if categoria is False:
            return response("error", "categoria ja existente", 403)
        
        return jsonify(categoria.to_dict()), 201
    except Exception as e:
        print(e)
        return response("error", "erro ao criar categoria", 500)
    
@categoria_bp.route("", methods=["GET"])
@jwt_required()
def read_categorias():
    categorias = listar_categorias()
    if categorias == []:
        return response("message", "sem categorias", 200)
    
    return jsonify([categoria.to_dict() for categoria in categorias]), 200