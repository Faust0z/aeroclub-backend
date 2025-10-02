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

    code = auto_field(required=True)


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


class AirportCodesUpdateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AirportCodes
        load_instance = False
        include_fk = False
        exclude = ()

    id = auto_field(dump_only=True)
    code = auto_field(required=True)
    itineraries = fields.Nested(ItinerariesSchema, many=True, dump_only=True)


class FlightSessionsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FlightSessions
        load_instance = True
        include_fk = False
        exclude = ("id",)

    issued_date = auto_field(dump_only=True)
    observations = auto_field(required=False, allow_none=True)
    flight_session_identifier = auto_field(dump_only=True)
    itineraries = fields.Nested(ItinerariesSchema, many=True)


class FlightSessionsAdminSchema(FlightSessionsSchema):
    @post_dump(pass_original=True)
    def group_users_by_role(self, data, flight_sessions):
        users = flight_sessions.users
        for user in users:
            for role in user.roles:
                key = role.name
                data[key] = UsersSchema().dump(user)
        return data


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


class PaymentTypesUpdateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PaymentTypes
        load_instance = False
        include_fk = False
        exclude = ("id",)

    type = auto_field(required=False)
    details = auto_field(required=False, allow_none=True)


class PlaneStatusSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PlaneStatus
        load_instance = True
        include_fk = False
        exclude = ("id",)

    state = auto_field(required=True)


class PlaneStatusUpdateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PlaneStatus
        load_instance = False
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


class PlanesUpdateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Planes
        load_instance = False
        include_fk = False
        exclude = ("id",)

    brand = auto_field(required=False)
    model = auto_field(required=False)
    registration = auto_field(required=False)
    category = auto_field(required=False)
    acquisition_date = auto_field(required=False, allow_none=True)
    consumption_per_hour = auto_field(required=False)
    description = auto_field(required=False, allow_none=True)


class RolesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Roles
        load_instance = True
        include_fk = False
        exclude = ("id", "users",)

    name = auto_field(required=True, dump_only=True)


class RolesUserUpdateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Roles
        load_instance = False
        include_fk = False
        exclude = ("id", "users",)

    name = auto_field(required=False, dump_only=True)


class RolesAdminUpdateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Roles
        load_instance = False
        include_fk = False
        exclude = ()

    id = auto_field(dump_only=True)
    name = auto_field(required=False)


class TransactionsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Transactions
        load_instance = True
        include_fk = False
        exclude = ("id",)

    amount = auto_field(required=True)
    issued_date = auto_field(required=True)
    description = auto_field(required=False, allow_none=True)
    payment_type = fields.Nested(PaymentTypesUpdateSchema, required=True)


class UsersRegisterSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True
        include_fk = False
        exclude = ("id", "created_at", "disabled_at", "status", "roles", "flight_sessions",)

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
        exclude = ("id", "flight_sessions", "disabled_at", "status", "password",)

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
        load_instance = False
        include_fk = False
        exclude = ("id", "flight_sessions", "disabled_at", "status",)

    first_name = auto_field(required=False)
    last_name = auto_field(required=False)
    phone_number = auto_field(required=False)
    address = auto_field(required=False, allow_none=True)
    password = auto_field(required=False, load_only=True)
    # plain dicts, not ORM
    roles = fields.Nested(RolesUserUpdateSchema, many=True, dump_only=True)


class UsersAdminUpdateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = False
        include_fk = False
        exclude = ("flight_sessions", "status",)

    id = auto_field(dump_only=True)
    first_name = auto_field(required=False)
    last_name = auto_field(required=False)
    phone_number = auto_field(required=False)
    address = auto_field(required=False, allow_none=True)
    email = auto_field(required=False)
    password = auto_field(required=False, load_only=True)
    # plain dicts, not ORM
    roles = fields.List(fields.Nested(RolesAdminUpdateSchema), required=False)


class UsersInstructorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True
        include_fk = False
        exclude = ("id", "flight_sessions", "address", "created_at", "disabled_at", "password", "roles")

    first_name = auto_field(required=True, dump_only=True)
    last_name = auto_field(required=True, dump_only=True)
    phone_number = auto_field(required=True, dump_only=True)
    email = auto_field(dump_only=True)
    status = auto_field(dump_only=True)


class UsersAdminSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True
        include_fk = False
        exclude = ("flight_sessions", "password",)

    first_name = auto_field(required=False)
    last_name = auto_field(required=False)
    phone_number = auto_field(required=False)
    address = auto_field(required=False, allow_none=True)
    email = auto_field(required=False)
    status = auto_field(required=False)
    roles = fields.Nested(RolesSchema, many=True, required=False)
