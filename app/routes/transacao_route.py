from flask import Blueprint, request, jsonify
from app.utils.response import response
from app.services.transacao_service import transacao, listar_transacoes

from flask_jwt_extended import jwt_required

transacao_bp = Blueprint("transacao", __name__, url_prefix="/transacoes")

@transacao_bp.route("", methods=["POST"])
@jwt_required()
def register():
    try:
        data = request.get_json()
        descricao = data.get("descricao")
        valor = data.get("valor")
        tipo = data.get("tipo")
        id_categoria = data.get("id_categoria")

        if not descricao:
            return response("error", "descricao obrigatoria", 400)
        if not valor:
            return response("error", "valor obrigatorio", 400)
        if not tipo:
            return response("error", "tipo obrigatorio", 400)
        if not id_categoria:
            return response("error", "categoria obrigatoria", 400)
        
        nova_transacao = transacao(
            descricao=descricao,
            valor=valor,
            tipo=tipo,
            id_categoria=id_categoria
        )
        if nova_transacao is None:
            return response("error", "categoria nao encontrada", 404)
        
        return jsonify(nova_transacao.to_dict()), 201
    except Exception as e:
        print(e)
        return response("error", "erro ao realizar transacao", 500)
    
@transacao_bp.route("", methods=["GET"])
@jwt_required()
def read_transacoes():
    transacoes = listar_transacoes()
    if transacoes == []:
        return response("message", "voce ainda nao realizou nenhuma transacao", 200)

    return jsonify([t.to_dict() for t in transacoes]), 200