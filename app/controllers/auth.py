from flask import Blueprint, request

auth_bp = Blueprint('auth', __name__)


# TODO: change the implementation to a JWT
@auth_bp.post('')
def authCrearYDevolverToken():
    pass
    # try:
    #     """
    #     data = request.get_json()
    #     email=data.get("email")
    #     nombre=data.get("nombre")
    #     apellido= data.get("apellido")
    #     telefono=data.get("telefono")
    #     dni=data.get("dni")
    #     direccion= data.get("direccion")
    #     """
    #     data = request.get_json()
    #     email = data.get("email")
    #
    #     usuarioController = UsuariosController()
    #     respuestaCrearUsuario = usuarioController.crearUsuario(data)
    #
    #     if respuestaCrearUsuario:
    #         rolesController = RolesController()
    #         respuestaRoles = rolesController.asignarAsociadoPorDefecto(email)
    #
    #         if respuestaRoles:
    #             encoded_token = Security.generate_token(email)
    #             return {'token': encoded_token, 'success': True}, 200
    #         else:
    #             return {'message': "No se pudo asignar el rol por defecto de Asociado", 'success': False}, 400
    #     else:
    #         return {'message': "No se pudo crear el usuario", 'success': False}, 400
    # except Exception as ex:
    #     print(ex)
    #     return {'message': "ERROR", 'success': False}, 401


@auth_bp.get('/<str:email>')
def chequearSiExisteUsuario(email: str):
    pass
    # try:
    #     usuarioController = UsuariosController()
    #     getUsuario = usuarioController.obtenerUsuarioPorEmail(email)
    #
    #     if not getUsuario:
    #         return {'message': "No se encontro un usuario con este email", 'success': False}, 404
    #
    #     encoded_token = Security.generate_token(email)
    #     return {'token': encoded_token, 'success': True}, 200
    # except Exception as ex:
    #     print(ex)
    #     return {'message': "ERROR", 'success': False}, 401


@auth_bp.get('')
def resolverToken():
    pass
    # try:
    #     dataToken = Security.resolvertoken(request.headers)
    #     if dataToken:
    #         return {'dataToken': dataToken, 'success': True}, 200
    #     else:
    #         return {'message': 'No existe un token valido', 'success': False}, 401
    # except Exception as ex:
    #     print(ex)
    #     return {'message': 'ocurrio un error', 'success': False}, 401
