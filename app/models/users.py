from ..extensions import db


class Users(db.Model):
    __tablename__ = "users"
    id_usuarios = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(45), nullable=False)
    apellido = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    telefono = db.Column(db.Integer, nullable=False)
    dni = db.Column(db.Integer, nullable=False, unique=True)
    fecha_alta = db.Column(db.Date, nullable=False)
    fecha_baja = db.Column(db.Date, nullable=False)
    direccion = db.Column(db.String(100))
    foto_perfil = db.Column(db.Text)
    estado_hab_des = db.Column(db.Integer, nullable=False)

    roles = db.relationship(
        "Roles", secondary="users_have_roles", back_populates="usuarios"
    )
