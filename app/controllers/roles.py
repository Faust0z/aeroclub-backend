from flask import Blueprint, request

from app.services.roles import editarRol, eliminarRol
from app.services.users import get_user_by_email_srv

roles_bp = Blueprint("roles", __name__, url_prefix='/roles')


@roles_bp.get("/")
def create_role_endp():
    try:
        data = request.get_json()
        respuesta = editarRol(data)
        if respuesta == 1:
            return {"error": "Ese rol no esta permitido"}, 400
        if respuesta == 2:
            return {"message": "Ya posee ese rol"}, 200
        if respuesta == 3:
            return {"message": "El rol se le asigno correctamente"}, 200
        if respuesta == 4:
            return {
                "error": "El mail no es válido y no esta asociado a una cuenta"
            }, 404
    except Exception as ex:
        print(ex)
        return {"error": "ocurrio un error"}, 401


@roles_bp.get("/<string:email>")
def get_user_roles_endp(email: str):
    try:
        getUsuario = get_user_by_email_srv(email=email, include_roles=True)

        if getUsuario:
            arrayRoles = []
            rolesGetUsuario = getUsuario.get("roles")
            for rol in rolesGetUsuario:
                arrayRoles.append(rol.get("tipo"))
            return {"roles": arrayRoles}, 200
        else:
            return {"error": "No se encontro un usuario con este email"}, 404
    except Exception as ex:
        print(ex)
        return {"error": "ocurrio un error"}, 401


@roles_bp.delete("/")
def delete_role_endp():
    try:
        data = request.get_json()
        respuesta = eliminarRol(data)
        if respuesta == 1:
            return {"error": "Ese rol no esta permitido"}, 400
        if respuesta == 2:
            return {"message": "Se elimino el rol correctamente"}, 200
        if respuesta == 3:
            return {
                "error": "El rol que quiere eliminar no lo posee, asi que no se realiza acciones"
            }, 400
        if respuesta == 4:
            return {
                "error": "El mail no es válido y no esta asociado a una cuenta"
            }, 404
    except Exception as ex:
        print(ex)
        return {"error": "ocurrio un error"}, 401
