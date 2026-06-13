from app.extensions import db
from app.enums.tipo_transacao import TipoTransacao

class Transacao(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    descricao = db.Column(db.String(255),  nullable=False)
    valor = db.Column(db.Float,  nullable=False)
    tipo = db.Column(
        db.Enum(TipoTransacao),
        default=TipoTransacao.DESPESA.value,
        nullable=False )
    data = db.Column(
        db.DateTime(),
        server_default=db.func.now()   
    )
    id_categoria = db.Column(
        db.Integer,
        db.ForeignKey("categoria.id"),
        nullable=False
    )
    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id"),
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "valor": self.valor,
            "tipo": TipoTransacao(self.tipo).value,
            "data": self.data,
            "id_usuario": self.id_usuario,
            "id_categoria": self.id_categoria
        }