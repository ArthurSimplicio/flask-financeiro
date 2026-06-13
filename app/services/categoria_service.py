from app.extensions import db
from app.models.categoria import Categoria

def criar_categoria(nome) -> Categoria:
    categoria = Categoria.query.filter_by(nome=nome).first()
    if categoria:
        return False
    
    nova_categoria = Categoria(nome=nome)

    db.session.add(nova_categoria)
    db.session.commit()

    return nova_categoria

def listar_categorias() -> list[Categoria]:
    categorias = Categoria.query.all()
    if len(categorias) == 0:
        return []
    
    return categorias