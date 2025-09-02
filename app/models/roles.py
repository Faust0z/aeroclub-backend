from ..extensions import db


class Roles(db.Model):
    __tablename__ = 'roles'
    id_roles = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(45))

    usuarios = db.relationship("Users", secondary="users_have_roles", back_populates="roles")
