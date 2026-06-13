from app.extensions import db
from app.models.transacao import Transacao
from app.models.categoria import Categoria
from app.enums.tipo_transacao import TipoTransacao

from flask_jwt_extended import get_jwt_identity

def transacao(
    descricao:str, 
    valor:float, 
    tipo:TipoTransacao, 
    id_categoria:int ) -> Transacao:
    id_usuario = get_jwt_identity()

    categoria = db.session.get(Categoria, id_categoria)
    if not categoria:
        return None

    nova_transacao = Transacao(
        descricao=descricao,
        valor=valor,
        tipo=TipoTransacao(tipo).value,
        id_categoria=id_categoria,
        id_usuario=int(id_usuario)
    )

    db.session.add(nova_transacao)
    db.session.commit()

    return nova_transacao

def listar_transacoes() -> list[Transacao]:
    id_usuario = get_jwt_identity()

    transacoes = Transacao.query.filter_by(id_usuario=id_usuario).all()
    if len(transacoes) == 0:
        return []
    
    return transacoes

from sqlalchemy import (func, case)

def obter_saldo():
    id_usuario = get_jwt_identity()

    resultado = db.session.query(
        func.sum(
            case((Transacao.tipo == TipoTransacao.RECEITA, Transacao.valor), else_=0)
        ).label("total_receitas"),
        func.sum(
            case((Transacao.tipo == TipoTransacao.DESPESA, Transacao.valor), else_=0)
        ).label("total_despesas")
    ).filter(Transacao.id_usuario == id_usuario).first()

    receitas = float(resultado.total_receitas or 0.0) 
    despesas = float(resultado.total_despesas or 0.0)
    saldo = receitas - despesas


    return {
        "receitas": receitas,
        "despesas": despesas,
        "saldo": saldo
    }



    