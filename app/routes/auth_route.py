from flask import Blueprint, request, jsonify
from app.utils.response import response
from app.services.auth_service import criar_usuario, logar

auth_bp = Blueprint("usuario", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        nome = data.get("nome")
        email = data.get("email")
        senha = data.get("senha")

        if not nome:
            return response("error", "nome obrigatorio", 400)
        if not email:
            return response("error", "email obrigatorio", 400)
        if not senha:
            return response("error", "senha obrigatoria", 400)
        
        usuario = criar_usuario(
            nome=nome,
            email=email,
            senha=senha
        )
        if usuario is False:
            return response("error", "email ja em uso", 400)
        
        return jsonify(usuario.to_dict()), 201
    except Exception as e:
        print(e)
        return response("error", "erro ao criar usuario", 500)
    
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        senha = data.get("senha")

        if not email:
            return response("error", "email obrigatorio", 400)
        if not senha:
            return response("error", "senha obrigatoria", 400)
        
        token = logar(email=email, senha=senha)
        if token is None:
            return response("error", "email invalido", 401)
        if token is False:
            return response("error", "senha invalida", 401)
        
        return jsonify({"token": token}), 200
    except Exception as e:
        print(e)
        return response("error", "erro ao logar usuario", 500)

from flask_jwt_extended import jwt_required
from app.services.transacao_service import obter_saldo
    
@auth_bp.route("/saldo", methods=["GET"])
@jwt_required()
def saldo():
    total = obter_saldo()
    return jsonify(total), 200