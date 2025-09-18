from datetime import datetime, UTC

from flask import Flask, request
from marshmallow import ValidationError as MarshmallowValidationError
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized, Forbidden, Conflict, HTTPException


class BadAuthRequest(BadRequest):
    description = "Email and password are required"


class AuthError(Unauthorized):
    description = "Authentication credentials were not provided or are invalid"


class PermissionDenied(Forbidden):
    description = "You do not have permission to access this resource"


class PermissionDeniedDisabledUser(Forbidden):
    description = "User account is disabled"


class BalanceNotFound(NotFound):
    description = "Balance not found for this user"


class PaymentTypeNotFound(NotFound):
    description = "Payment type not found"


class PlaneNotFound(NotFound):
    description = "Plane not found"


class PaymentTypeAlreadyExists(Conflict):
    description = "Resource already exists"


class PlaneStatusAlreadyExists(Conflict):
    description = "Resource already exists"


class PlaneRegistrationAlreadyExists(Conflict):
    description = "Plane's registration already exists"


class ResourceAlreadyExists(Conflict):
    description = "Resource already exists"


class EmailAlreadyExists(Conflict):
    description = "The email given is already registered"


class UserNotFound(NotFound):
    description = "No user found with the given email"


class RoleNotFound(NotFound):
    description = "The given user does not posses the requested role"


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException) -> tuple[dict, int]:
        response: dict = {
            "error": e.__class__.__name__,
            "message": e.description,
            "status": e.code,
            "path": request.path,
            "timestamp": datetime.now(UTC).isoformat()
        }
        return response, e.code

    @app.errorhandler(Exception)  # catches any unhandled exception
    def handle_generic_error(e: Exception) -> tuple[dict, int]:
        response: dict = {
            "error": "InternalServerError",
            "message": str(e) or "An unexpected error occurred",
            "status": 500,
            "path": request.path,
            "timestamp": datetime.now(UTC).isoformat()
        }
        return response, 500

    @app.errorhandler(MarshmallowValidationError)
    def handle_marshmallow_error(e: MarshmallowValidationError) -> tuple[dict, int]:
        response: dict = {
            "error": "ValidationError",
            "message": e.messages,
            "status": 400,
            "path": request.path,
            "timestamp": datetime.now(UTC).isoformat()
        }
        return response, 400
