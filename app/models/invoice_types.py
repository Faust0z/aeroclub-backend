from ..extensions import db


class receipt_types(db.Model):
    __tablename__ = "receipt_types"
    id_tipo_recibos = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(45), nullable=False)
