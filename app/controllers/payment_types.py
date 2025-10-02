from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt
from marshmallow import ValidationError

from ..errors import PermissionDeniedDisabledUser, PermissionDenied
from ..extensions import db
from ..schemas import PaymentTypesSchema, PaymentTypesUpdateSchema
from ..services.payment_types import get_payment_types_srv, update_payment_type_srv

payment_types_bp = Blueprint("payment_types", __name__, url_prefix="/v1/payment_types")


@payment_types_bp.get("/")
@jwt_required()
def get_payment_types_endp():
    jwt_data = get_jwt()
    if not jwt_data.get("status", True):
        raise PermissionDeniedDisabledUser

    payment_types = get_payment_types_srv()

    schema = PaymentTypesSchema(many=True)
    return {"data": schema.dump(payment_types)}, 200


@payment_types_bp.patch("/<string:name>")
@jwt_required()
def update_payment_type_endp(name: str):
    jwt_data = get_jwt()
    caller_roles = jwt_data.get("roles", ["User"])
    if not "Admin" in caller_roles:
        raise PermissionDenied

    schema = PaymentTypesUpdateSchema(session=db.session, partial=True)
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return {"errors": err.messages}, 400
    payment_type = update_payment_type_srv(name=name, data=data)
    return {"data": schema.dump(payment_type)}, 200
