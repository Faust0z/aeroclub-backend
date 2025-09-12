from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from datetime import date

from .roles import get_role_by_name_srv
from ..models import Users, Roles
from ..services.balances import create_balance_srv
from ..extensions import db


def get_users_srv(email: str | None = None, first_name: str | None = None, last_name: str | None = None,
                  role_name: str | None = None, include_inactive: bool = False) -> list[Users]:
    stmt = db.select(Users).options(joinedload(Users.roles))

    if email:
        stmt = stmt.where(Users.email == email)
    if first_name:
        stmt = stmt.where(Users.first_name.ilike(f"%{first_name}%"))
    if last_name:
        stmt = stmt.where(Users.last_name.ilike(f"%{last_name}%"))
    if role_name:
        stmt = stmt.join(Users.roles).where(Roles.name == role_name)
    if not include_inactive:
        stmt = stmt.where(Users.status != 0)

    return db.session.execute(stmt).unique().scalars().all()


def get_user_by_email_srv(email: str = None, include_roles: bool = False) -> Users:
    stmt = db.select(Users)
    stmt = stmt.where(Users.email == email)

    if include_roles:
        stmt = stmt.options(joinedload(Users.roles))

    return db.session.scalar(stmt)


def editarUsuario(email, data):
    # solo trae el dicc y no la clase de la bd
    user = obtenerUsuarioPorEmail(email)
    # te trae un usuario de la bd
    usuario = Users.query.get(user["id_usuarios"])

    if not usuario:
        return False

    if 'nombre' in data:
        usuario.first_name = data['nombre']
    if 'apellido' in data:
        usuario.last_name = data['apellido']
    if 'email' in data:
        usuario.email = data['email']
    if 'telefono' in data:
        usuario.phone_number = data['telefono']
    if 'dni' in data:
        usuario.dni = data['dni']
    if 'fecha_alta' in data:
        usuario.created_at = data['fecha_alta']
    if 'fecha_baja' in data:
        usuario.disabled_at = data['fecha_baja']
    if 'direccion' in data:
        usuario.address = data['direccion']
    if 'foto_perfil' in data:
        usuario.foto_perfil = data['foto_perfil']
    if 'estado_hab_des' in data:
        usuario.status = data['estado_hab_des']

    # para que te lo guarde primero hay que buscar en la db una clase del modelo
    # y despues cuando modifique un atributo de esa clase cuenta como que lo modifique
    # y ahi el commit me lo toma como un cambio y lo guarda
    db.session.commit()
    return True


def eliminarUsuario(email):
    user = get_user_by_email_srv(email)

    if not user:
        return False

    with db.session.begin():
        user.status = False
        return True


def register_user_srv(user: Users) -> tuple[bool, str]:
    user.password = generate_password_hash(user.password)
    user.created_at = date.today()
    user.roles = get_role_by_name_srv("User")
    user.status = True

    db.session.add(user)
    db.session.flush()  # To make sure we can get the ID

    create_balance_srv(balance=0, user_id=user.id)
    db.session.commit()
    return True, "User created successfully"


def authenticate_user_srv(email: str, password: str) -> Users | None:
    user = get_user_by_email_srv(email)
    if not user or not check_password_hash(user.password, password):
        return None
    return user
