from flask import Blueprint, request
from ..services.users import obtenerUsuarios, obtenerUsuarioPorEmail, obtenerUsuarioPorNombre, crearUsuario, editarUsuario, \
    eliminarUsuario

users_bp = Blueprint("users", __name__)


# GET /users?role=instructor
@users_bp.get("/")
def get_users(role: str | None = None, email: str | None = None, nombre: str | None = None):
    try:
        # TODO: this surely can be furter simplified into a single method
        if role:
            usuarios = obtenerUsuariosPorRol(role)
        elif email:
            usuarios = obtenerUsuarioPorEmail(email)
        elif nombre:
            usuarios = obtenerUsuarioPorNombre(nombre)
        else:
            usuarios = obtenerUsuarios()

        if usuarios:
            return {"respuesta": usuarios}, 200
        else:
            return {"error": "No se encontraron usuarios"}, 404
    except Exception as ex:
        print(ex)
        return {"error": "ERROR"}, 500


@users_bp.get("/<str:email>")
def get_user_endp(email: str):
    try:
        usuario = obtenerUsuarioPorEmail(email)

        if usuario:
            return {"respuesta": usuario}, 200
        else:
            return {"error": "El usuario con ese email no existe"}, 404
    except Exception as ex:
        print(ex)
        return {"error": "ERROR"}, 401


@users_bp.post("/")
def create_user_endp():
    try:
        data = request.get_json()
        respuesta = crearUsuario(data)

        if respuesta == True:
            return {"message": "User created successfully"}, 201
        else:
            return {"error": "Algunos datos ingresados estan mal"}, 400
    except Exception as ex:
        print(ex)
        return {"error": "ocurrio un error"}, 401


# Ruta para actualizar un usuario por Email
@users_bp.patch("/<str:email>")
def update_user_endp(email: str):
    try:
        data = request.get_json()

        if editarUsuario(email, data):
            return {"message": "Usuario actualizado correctamente"}, 200
        else:
            return {"error": "Usuario no encontrado"}, 404
    except Exception as ex:
        print(ex)
        return {"error": "ocurrio un error"}, 401


@users_bp.delete("/<str:email>")
def delete_usuario_endp(email: str):
    try:

        if eliminarUsuario(email):
            return {"message": "Usuario actualizado correctamente"}, 200
        else:
            return {"error": "Usuario no encontrado"}, 404
    except Exception as ex:
        print(ex)
        return {"error": "ocurrio un error"}, 401
