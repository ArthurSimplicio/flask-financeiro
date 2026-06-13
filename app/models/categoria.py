from app.extensions import db

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String(255),  nullable=False)
    transacoes = db.relationship(
        "Transacao",
        backref="categoria",
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome
        }