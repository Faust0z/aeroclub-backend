from ..extensions import db


class PlaneStatus(db.Model):
    __tablename__ = "plane_status"
    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state: db.Mapped[str] = db.Column(db.String, unique=True)

    plane: db.Mapped[list["Planes"]] = db.relationship(back_populates="plane_status")

    def __repr__(self):
        return f"State=<{self.state}>"
