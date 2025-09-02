from ..extensions import db
from sqlalchemy import ForeignKey


class Planes(db.Model):
    __tablename__ = 'planes'
    id: db.Mapped[int] = db.mapped_column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    brand: db.Mapped[str] = db.mapped_column(db.String, nullable=False)
    model: db.Mapped[str] = db.mapped_column(db.String, nullable=False)
    registration: db.Mapped[str] = db.mapped_column(db.String, nullable=False, unique=True)
    category: db.Mapped[str] = db.mapped_column(db.String, nullable=False)
    acquisition_date: db.Mapped[db.Date] = db.mapped_column(db.Date, nullable=False)
    consumption_per_hour: db.Mapped[int] = db.mapped_column(db.Integer, nullable=False)
    description: db.Mapped[str] = db.mapped_column(db.Text)
    plane_status_id: db.Mapped[int] = db.mapped_column(db.Integer, ForeignKey('plane_status.id_estados_aeronaves'))

    def __repr__(self):
        return (
            f"<Plane(id={self.id}, brand='{self.brand}', model='{self.model}', "
            f"registration='{self.registration}', power='{self.power}', "
            f"category='{self.category}', acquisition_date={self.acquisition_date}, "
            f"consumption_per_hour={self.consumption_per_hour}, "
            f"documentation_path='{self.documentation_path}', "
            f"description='{self.description}'"
            f"plane_status_id={self.plane_status_id})>"
        )
