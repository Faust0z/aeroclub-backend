from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt
from marshmallow import ValidationError

from ..errors import PermissionDeniedDisabledUser, PermissionDenied
from ..schemas import PlaneStatusSchema, PlaneStatusUpdateSchema
from ..services.plane_status import get_planes_status_srv, update_plane_status_srv

plane_status_bp = Blueprint("plane_status", __name__, url_prefix="/v1/plane_status")


@plane_status_bp.get("/")
@jwt_required()
def get_plane_status_endp():
    jwt_data = get_jwt()
    if not jwt_data.get("status", True):
        raise PermissionDeniedDisabledUser

    plane_status = get_planes_status_srv()

    schema = PlaneStatusSchema(many=True)
    return {"data": schema.dump(plane_status)}, 200


@plane_status_bp.patch("/<string:name>")
@jwt_required()
def update_plane_status_endp(name: str):
    jwt_data = get_jwt()
    caller_roles = jwt_data.get("roles", ["User"])
    if not "Admin" in caller_roles:
        raise PermissionDenied

    schema = PlaneStatusUpdateSchema(partial=True)
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return {"errors": err.messages}, 400
    plane_status = update_plane_status_srv(name=name, data=data)
    return {"data": schema.dump(plane_status)}, 200
