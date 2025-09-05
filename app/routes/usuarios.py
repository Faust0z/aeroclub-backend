from flask import Blueprint, request, jsonify
from app.controllers.users import UsuariosController

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/", methods=["GET"])
def get_users():
    try:
        usuarioController = UsuariosController()
        usuarios = usuarioController.obtenerUsuarios()

        if usuarios:
            return jsonify({"respuesta": usuarios, "success": True})
        else:
            jsonify({"message": "No se encontraron usuarios", "success": False})
    except Exception as ex:
        print(ex)
        return jsonify({"message": "ERROR", "success": False})


@usuarios_bp.route("/<email>", methods=["GET"])
def getUsuarioByEmail(email):
    try:
        usuarioController = UsuariosController()
        usuario = usuarioController.obtenerUsuarioPorEmail(email)

        if usuario:
            return jsonify({"respuesta": usuario, "success": True})
        else:
            return jsonify(
                {"message": "El usuario con ese email no existe", "success": False}
            )
    except Exception as ex:
        print(ex)
        return jsonify({"message": "ERROR", "success": False})


# Obtener todos los Intructores
@usuarios_bp.route("/instructores", methods=["GET"])
def get_instructor():
    try:
        usuarioController = UsuariosController()
        usuarios = usuarioController.obtenerInstructores()

        if usuarios:
            return jsonify({"respuesta": usuarios, "success": True})
        else:
            jsonify({"message": "No se encontraron usuarios", "success": False})
    except Exception as ex:
        print(ex)
        return jsonify({"message": "ERROR", "success": False})


# Obtener todos los Asociados
@usuarios_bp.route("/asociados", methods=["GET"])
def get_asociados():
    try:
        usuarioController = UsuariosController()
        usuarios = usuarioController.obtenerAsociados()

        if usuarios:
            return jsonify({"respuesta": usuarios, "success": True})
        else:
            jsonify({"message": "No se encontraron usuarios", "success": False})
    except Exception as ex:
        print(ex)
        return jsonify({"message": "ERROR", "success": False})


@usuarios_bp.route("/", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        usuarioController = UsuariosController()
        respuesta = usuarioController.crearUsuario(data)

        if respuesta == True:
            return (
                jsonify({"message": "User created successfully", "success": True}),
                201,
            )
        else:
            return (
                jsonify({"message": "Algunos datos ingresados estan mal"}),
                400,
            )
    except Exception as ex:
        print(ex)
        return jsonify({"message": "ocurrio un error", "success": False})


# Ruta para actualizar un usuario por Email
@usuarios_bp.route("/<email>", methods=["PATCH"])
def update_user(email):
    try:
        data = request.get_json()
        usuarioControler = UsuariosController()

        if usuarioControler.editarUsuario(email, data):
            return jsonify(
                {"mensaje": "Usuario actualizado correctamente", "success": True}
            )
        else:
            return (
                jsonify({"mensaje": "Usuario no encontrado", "success": False}),
                404,
            )
    except Exception as ex:
        print(ex)
        return jsonify({"message": "ocurrio un error", "success": False})


# Ruta para "borrar" un usuario por email
@usuarios_bp.route("/<email>", methods=["DELETE"])
def delete_usuario(email):
    try:
        usuarioControler = UsuariosController()

        if usuarioControler.eliminarUsuario(email):
            return jsonify(
                {"mensaje": "Usuario actualizado correctamente", "success": True}
            )
        else:
            return (
                jsonify({"mensaje": "Usuario no encontrado", "success": False}),
                404,
            )
    except Exception as ex:
        print(ex)
        return jsonify({"message": "ocurrio un error", "success": False})


@usuarios_bp.route("/nombre/<nombre>", methods=["GET"])
def getUsuarioByNombre(nombre):
    try:
        usuarioController = UsuariosController()

        if usuarioController.obtenerUsuarioPorNombre(nombre):
            return jsonify(
                {
                    "respuesta": usuarioController.obtenerUsuarioPorNombre(nombre),
                    "success": True,
                }
            )
        else:
            return jsonify(
                {
                    "message": "No existe usuario con esa combinación",
                    "success": False,
                }
            )
    except Exception as ex:
        print(ex)
        return jsonify({"message": "ERROR", "success": False})
