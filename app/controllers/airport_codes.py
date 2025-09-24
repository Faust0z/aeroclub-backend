from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt

from ..errors import PermissionDeniedDisabledUser, PermissionDenied
from ..extensions import db
from ..schemas import AirportCodesSchema
from ..services.airport_codes import get_airport_codes_srv, update_airport_code_srv, get_airport_code_by_code_srv

airport_codes_bp = Blueprint("airport_codes", __name__, url_prefix="/v1/airport_codes")


@airport_codes_bp.get("/")
@jwt_required()
def get_airport_codes_endp():
    jwt_data = get_jwt()
    if not jwt_data.get("status", True):
        raise PermissionDeniedDisabledUser

    airport_codes = get_airport_codes_srv()

    schema = AirportCodesSchema(many=True)
    return {"data": schema.dump(airport_codes)}, 200


@airport_codes_bp.get("/<string:code>")
@jwt_required()
def get_airport_code_by_code_endp(code: str):
    jwt_data = get_jwt()
    if not jwt_data.get("status", True):
        raise PermissionDeniedDisabledUser

    airport_code = get_airport_code_by_code_srv(code=code)

    schema = AirportCodesSchema(many=True)
    return {"data": schema.dump(airport_code)}, 200


@airport_codes_bp.put("/<string:code>")
@jwt_required()
def update_airport_code_endp(code: str):
    jwt_data = get_jwt()
    caller_roles = jwt_data.get("roles", ["User"])
    if not "Admin" in caller_roles:
        raise PermissionDenied

    schema = AirportCodesSchema(session=db.session, partial=True)
    data = schema.load(request.get_json())
    airport_code = update_airport_code_srv(code=code, data=data)
    return {"data": schema.dump(airport_code)}, 200
