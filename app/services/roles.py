from app.models.users import Users
from app.models.roles import Roles
from ..extensions import db


def get_role_by_name_srv(name: str) -> Roles:
    return db.session.scalars(db.select(Roles).where(Roles.name == name)).all()


def __chequearArrayRoles(roles, rol):
    resultado = [x for x in roles if x.get("tipo") == rol]

    if resultado:
        return True
    else:
        return False


def __chequearRolesPermitidos(rol):
    rolesPermitidos = ["Asociado", "Gestor", "Instructor"]

    resultado = [x for x in rolesPermitidos if x == rol]
    if resultado:
        return True
    else:
        return False


def editarRol(data):
    # Obtenemos el userDictionary
    userDictionary = obtenerUsuarioPorEmail(None, data.get("email"))

    try:
        if __chequearRolesPermitidos(data.get("rol")):
            if __chequearArrayRoles(userDictionary.get("roles"), data.get("rol")):
                return 2
            else:
                # nos traemos la data del rol que se paso por el endpoint
                rol = data.get("rol")
                rolDictionary = db.session.execute(
                    db.select(Roles).filter_by(tipo=rol)
                ).scalar_one()
                # creo el usuarioTieneRoles

                # TODO: this broke down when the associations where changed to Tables
                # usuarioTieneRoles = UsersHaveRoles(
                #    0, userDictionary.get("id_usuarios"), rolDictionary.id
                # )
                # db.session.add(usuarioTieneRoles)
                db.session.commit()
                return 3
        else:
            return 1

    except Exception as ex:
        print(ex)
        return 4


def eliminarRol(data):
    # Obtenemos el userDictionary
    userDictionary = obtenerUsuarioPorEmail(None, data.get("email"))

    try:
        if __chequearRolesPermitidos(data.get("rol")):
            if __chequearArrayRoles(
                    userDictionary.get("roles"), data.get("rol")
            ):
                rolData = data.get("rol")
                id_usuario = userDictionary.get("id_usuarios")
                rolEncontrado = db.session.execute(
                    db.select(Roles).filter_by(tipo=rolData)
                ).scalar_one()

                rol_id = rolEncontrado.id

                # TODO: this broke down when the associations where changed to Tables
                #                    usuarioTieneRoles = db.session.execute(
                #                        db.select(UsersHaveRoles).filter_by(
                #                            usuarios_id=id_usuario, roles_id=rol_id
                #                       )
                #                   ).scalar_one()
                #
                #                    db.session.delete(usuarioTieneRoles)
                db.session.commit()
                return 2
            else:
                return 3
        else:
            return 1
    except Exception as ex:
        print(ex)
        return 4
