from ..extensions import db
from .associations import users_have_roles


class Roles(db.Model):
    __tablename__ = 'roles'
    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: db.Mapped[str] = db.Column(db.String, nullable=False, unique=True)

    users: db.Mapped["Users"] = db.relationship(secondary=users_have_roles, back_populates="roles")

    def __repr__(self):
        return f"<Role name={self.name}>"
