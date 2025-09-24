from marshmallow import fields, validate, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from .models import Users, Roles, Transactions, Planes, PlaneStatus, PaymentTypes, ItineraryTypes, Itineraries, \
    FlightSessions, Fares, \
    Balances, AirportCodes


class AirportCodesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AirportCodes
        load_instance = True
        include_fk = False
        exclude = ("id", "itineraries",)


class BalancesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Balances
        load_instance = True
        include_fk = False
        exclude = ("id",)

    balance: auto_field(required=True, dump_only=True)


# So admins can CRUD balances
class BalancesAdminSchema(BalancesSchema):
    exclude = ()
    id = auto_field(dump_only=True)
    balance: auto_field(required=False)


class FaresSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Fares
        load_instance = True
        include_fk = False
        exclude = ("id",)

    issued_date = auto_field(required=True, dump_only=True)
    fare_value = auto_field(required=True, dump_only=True)


class FaresAdminSchema(FaresSchema):
    exclude = ()
    id = auto_field(dump_only=True)
    issued_date = auto_field(required=False)
    fare_value = auto_field(required=False)


class ItinerariesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Itineraries
        load_instance = True
        include_fk = False
        exclude = ("id",)

    departure_time = auto_field(required=True)
    arrival_time = auto_field(required=True)
    landings_amount = auto_field(required=True)
    observations = auto_field(required=False, allow_none=True)
    airport_codes = fields.Nested(AirportCodesSchema, many=True)


# Includes itineraries and excludes airport_codes to avoid circular nesting
class AirportCodesWithItinerariesSchema(AirportCodesSchema):
    itineraries = fields.Nested(ItinerariesSchema, many=True, exclude=("airport_codes",))


class ItineraryTypesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ItineraryTypes
        load_instance = True
        include_fk = False
        exclude = ("id",)

    type = auto_field(required=True)


class PaymentTypesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PaymentTypes
        load_instance = True
        include_fk = False
        exclude = ("id",)

    type = auto_field(required=True)
    details = auto_field(required=False, allow_none=True)


class PlaneStatusSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PlaneStatus
        load_instance = True
        include_fk = False
        exclude = ("id",)

    state = auto_field(required=True)


class PlanesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Planes
        load_instance = True
        include_fk = False
        exclude = ("id",)

    brand = auto_field(required=True)
    model = auto_field(required=True)
    registration = auto_field(required=True)
    category = auto_field(required=True)
    acquisition_date = auto_field(required=False, allow_none=True)
    consumption_per_hour = auto_field(required=True)
    description = auto_field(required=False, allow_none=True)


class RolesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Roles
        load_instance = True
        include_fk = False
        exclude = ("id", "users",)

    name = auto_field(required=True, dump_only=True)


# So admins can CRUD roles
class RolesAdminSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Roles
        load_instance = True
        include_fk = False
        exclude = ()

    id = auto_field(dump_only=True)
    name = auto_field(required=False)
    users = fields.Nested(RolesSchema, many=True, dump_only=True)


class TransactionsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Transactions
        load_instance = True
        include_fk = False
        exclude = ("id",)

    amount = auto_field(required=True)
    issued_date = auto_field(required=True)
    description = auto_field(required=False, allow_none=True)
    payment_type = fields.Nested(PaymentTypesSchema, required=True)


class UsersRegisterSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True
        include_fk = False
        exclude = ("id", "created_at", "disabled_at", "status", "roles", "invoices",)

    first_name = auto_field(required=True)
    last_name = auto_field(required=True)
    phone_number = auto_field(required=True)
    address = auto_field(required=False, allow_none=True)
    email = auto_field(required=True)
    password = auto_field(required=True, load_only=True, validate=validate.Length(min=8))


class UsersSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True
        include_fk = False
        exclude = ("id", "invoices", "disabled_at", "status", "password",)

    first_name = auto_field(required=True)
    last_name = auto_field(required=True)
    phone_number = auto_field(required=True)
    address = auto_field(required=False, allow_none=True)
    email = auto_field(dump_only=True)
    created_at = auto_field(dump_only=True)
    roles = fields.Nested(RolesSchema, many=True, dump_only=True)


class UsersUpdateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True
        include_fk = False
        exclude = ("id", "invoices", "disabled_at", "status", "password",)

    first_name = auto_field(required=False)
    last_name = auto_field(required=False)
    phone_number = auto_field(required=False)
    address = auto_field(required=False, allow_none=True)


class UsersInstructorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True
        include_fk = False
        exclude = ("id", "invoices", "address", "created_at", "disabled_at", "password",)

    first_name = auto_field(required=True, dump_only=True)
    last_name = auto_field(required=True, dump_only=True)
    phone_number = auto_field(required=True, dump_only=True)
    email = auto_field(dump_only=True)
    status = auto_field(dump_only=True)
    roles = fields.Nested(RolesSchema, many=True, dump_only=True)


class UsersAdminSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True
        include_fk = False
        exclude = ("invoices", "password",)

    first_name = auto_field(required=False)
    last_name = auto_field(required=False)
    phone_number = auto_field(required=False)
    address = auto_field(required=False, allow_none=True)
    email = auto_field(required=False)
    status = auto_field(required=False)
    roles = fields.Nested(RolesSchema, many=True, required=False)
