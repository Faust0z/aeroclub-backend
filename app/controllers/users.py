from flask import Blueprint, request
from ..services.users import obtenerUsuarios, obtenerUsuarioPorEmail, obtenerUsuarioPorNombre, crearUsuario, editarUsuario, \
    eliminarUsuario

users_bp = Blueprint("users", __name__)


@users_bp.get("/")
@jwt_required()
def get_users_endp():
    try:
        # Filters
        role = request.args.get("role")
        email = request.args.get("email")
        first_name = request.args.get("first_name")
        last_name = request.args.get("last_name")
        jwt_data = get_jwt()
        caller_roles = jwt_data.get("roles", ["User"])

        usuarios = get_users_srv(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role_name=role
        )

        if usuarios:
            if caller_roles == "Admin":
                schema = UsersAdminSchema(many=True)
            elif caller_roles == "Instructor":
                schema = UsersInstructorSchema(many=True)
            else:
                schema = UsersSchema(many=True)

            return {"respuesta": schema.dump(usuarios)}, 200
        else:
            return {"error": "No users found"}, 404
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


@users_bp.post("/register")
def register_user_endp():
    schema = UserRegisterSchema(session=db.session)
    try:
        data = schema.load(request.get_json())
        success, msg = register_user_srv(data)

        if success:
            return {"message": msg}, 201
        else:
            return {"error": msg}, 409
    except ValidationError as err:
        return {"errors": err.messages}, 400


@users_bp.post("/login")
def login_endp():
    email = request.json.get("email")
    password = request.json.get("password")

    user = authenticate_user_srv(email, password)
    if not user:
        return {"msg": "Bad credentials"}, 401

    roles = [role.name for role in user.roles] if user.roles else ["User"]
    additional_claims = {"roles": roles}

    access_token = create_access_token(
        identity=user.email,
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=24)
    )

    return {"access_token": access_token}, 200
