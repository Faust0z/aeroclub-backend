from .associations import users_have_roles, users_have_invoices
from ..extensions import db
from datetime import date


class Users(db.Model):
    __tablename__ = "users"
    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name: db.Mapped[str] = db.Column(db.String, nullable=False)
    last_name: db.Mapped[str] = db.Column(db.String, nullable=False)
    email: db.Mapped[str] = db.Column(db.String, nullable=False, unique=True)
    phone_number: db.Mapped[str] = db.Column(db.String, nullable=False)
    created_at: db.Mapped[date] = db.Column(db.Date, nullable=False)
    disabled_at: db.Mapped[date] = db.Column(db.Date, nullable=False)
    address: db.Mapped[str] = db.Column(db.String)
    status: db.Mapped[bool] = db.Column(db.Boolean, nullable=False)
    role_id = db.mapped_column(db.ForeignKey("roles.id"), nullable=False)

    roles: db.Mapped["Roles"] = db.relationship(secondary=users_have_roles, back_populates="roles")
    invoices: db.Mapped[list["Invoices"]] = db.relationship(secondary=users_have_invoices, back_populates="invoices")

    def __repr__(self):
        return f"<first_name={self.first_name} email={self.email}>"
