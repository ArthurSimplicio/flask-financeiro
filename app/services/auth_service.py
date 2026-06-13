from app.extensions import db
from app.models.usuario import Usuario

from werkzeug.security import generate_password_hash, check_password_hash

def criar_usuario(nome:str, email:str, senha:str) -> Usuario:
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario:
        return False
    
    hashed_senha = generate_password_hash(senha, salt_length=100)
    
    novo_usuario = Usuario(
        nome=nome,
        email=email,
        senha=hashed_senha
    )

    db.session.add(novo_usuario)
    db.session.commit()

    return novo_usuario

from flask_jwt_extended import create_access_token

def logar(email:str, senha:str):
    usuario:Usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        return None
    
    if not check_password_hash(usuario.senha, senha):
        return False

    token = create_access_token(
        identity=str(usuario.id)
    )

    return token