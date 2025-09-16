from datetime import timedelta

from flask import Blueprint, request
from flask_jwt_extended import get_jwt, create_access_token, jwt_required
from sqlalchemy.exc import IntegrityError

from ..errors import EmailAlreadyExists, UserNotFound, AuthError, PermissionDenied, BadAuthRequest, PermissionDeniedDisabledUser
from ..extensions import db
from ..schemas import UsersRegisterSchema, UsersSchema, UsersAdminSchema, UsersInstructorSchema, UsersUpdateSchema
from ..services.users import get_users_srv, register_user_srv, update_user_srv, disable_user_srv, authenticate_user_srv, \
    get_user_by_email_srv

users_bp = Blueprint("users", __name__, url_prefix='/users')


@users_bp.get("/")
@jwt_required()
def get_users_endp():
    jwt_data = get_jwt()
    if not jwt_data.get("status", True):
        raise PermissionDeniedDisabledUser

    caller_roles = jwt_data.get("roles", ["User"])
    if "Admin" in caller_roles:
        schema = UsersAdminSchema(many=True)
    elif "Instructor" in caller_roles:
        schema = UsersInstructorSchema(many=True)
    else:
        raise PermissionDenied

    # Filters
    role = request.args.get("role")
    email = request.args.get("email")
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    users = get_users_srv(
        email=email,
        first_name=first_name,
        last_name=last_name,
        role_name=role
    )

    return {"data": schema.dump(users)}, 200


@users_bp.get("/me")
@jwt_required()
def get_my_info_endp():
    jwt_data = get_jwt()
    if not jwt_data.get("status", True):
        raise PermissionDeniedDisabledUser

    user_email = jwt_data["sub"]

    user = get_user_by_email_srv(user_email)
    if not user:
        raise UserNotFound

    schema = UsersSchema()
    return {"data": schema.dump(user)}, 200


@users_bp.get("/<string:email>")
@jwt_required()
def get_user_by_email_endp(email: str):
    jwt_data = get_jwt()
    if not jwt_data.get("status", True):
        raise PermissionDeniedDisabledUser

    caller_roles = jwt_data.get("roles", ["User"])
    if "Admin" in caller_roles:
        schema = UsersAdminSchema(many=True)
    elif "Instructor" in caller_roles:
        schema = UsersInstructorSchema(many=True)
    else:
        schema = UsersSchema(many=True)

    user = get_user_by_email_srv(email=email)
    if not user:
        raise UserNotFound()

    return {"data": schema.dump(user)}, 200


@users_bp.patch("/<string:email>")
@jwt_required()
def update_user_endp(email: str):
    jwt_data = get_jwt()
    if not jwt_data.get("status", True):
        raise PermissionDeniedDisabledUser

    caller_roles = jwt_data.get("roles", ["User"])
    if "Admin" in caller_roles:
        schema = UsersAdminSchema(partial=True)
    else:
        schema = UsersUpdateSchema(partial=True)

    data = schema.load(request.get_json())
    user = update_user_srv(email, data)
    if not user:
        raise UserNotFound()

    return {"data": schema.dump(user)}, 200


@users_bp.delete("/<string:email>")
@jwt_required()
def delete_user_endp(email: str):
    jwt_data = get_jwt()
    if not jwt_data.get("status", True):
        raise PermissionDeniedDisabledUser

    caller_roles = jwt_data.get("roles", ["User"])
    if "Admin" in caller_roles:
        user = disable_user_srv(email=email)
        if not user:
            raise UserNotFound

        return {"msg": "User disabled successfully"}, 200
    else:
        raise PermissionDenied


@users_bp.post("/register")
def register_user_endp():
    schema = UsersRegisterSchema(session=db.session)
    data = schema.load(request.get_json())

    try:
        user = register_user_srv(data)
        return {"msg": "User created successfully", "data": schema.dump(user)}, 201
    except IntegrityError:
        raise EmailAlreadyExists()


@users_bp.post("/login")
def login_endp():
    email = request.json.get("email")
    password = request.json.get("password")

    if not email and password:
        raise BadAuthRequest

    user = authenticate_user_srv(email, password)
    if not user:
        raise AuthError

    if not user.status:
        raise

    roles = [role.name for role in user.roles] if user.roles else ["User"]
    additional_claims = {
        "roles": roles,
        "status": user.status
    }

    access_token = create_access_token(
        identity=user.email,
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=24)
    )

    return {
        "msg": "Login successful",
        "access_token": access_token,
        "user": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "roles": roles
        }
    }, 200
