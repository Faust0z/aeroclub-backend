from ..extensions import db


class Invoices(db.Model):
    __tablename__ = "invoices"
    id_recibos = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.Date, nullable=False)
    observaciones = db.Column(db.Text)
    tipo_recibos_id = db.Column(db.Integer, db.ForeignKey("receipt_types.id_tipo_recibos"))
    transacciones_id = db.Column(db.Integer, db.ForeignKey("transactions.id_transacciones"))
    numero_recibos = db.Column(db.Integer, nullable=False)

    # usuarios = db.relationship("Users", secondary="USUARIOS_tienen_RECIBOS", back_populates="recibos")
    recibosTransacciones = db.relationship("Transactions", back_populates="transaccionesRecibos")
    # para borrar en cascada
    recibosItinerarios = db.relationship(
        "Itineraries",
        back_populates="itinerariosRecibos",
        cascade="all, delete-orphan",
        single_parent=True,
    )
