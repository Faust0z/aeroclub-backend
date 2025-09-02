from ..extensions import db


class PlaneStatus(db.Model):
    __tablename__ = "plane_status"
    id_estados_aeronaves = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estado = db.Column(db.String(45))
