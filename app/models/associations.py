from ..extensions import db

itinerary_has_airport_codes = db.Table(
    "itinerary_has_airport_codes",
    db.Column("itinerary_id", db.ForeignKey("itineraries.id"), primary_key=True),
    db.Column("aeroport_codes_id", db.ForeignKey("airport_codes.id"), primary_key=True),
)

users_have_roles = db.Table(
    "users_have_roles",
    db.Column("users_id", db.ForeignKey("users.id"), primary_key=True),
    db.Column("roles_id", db.ForeignKey("roles.id"), primary_key=True),
)

users_have_flight_sessions = db.Table(
    "users_have_flight_sessions",
    db.Column("users_id", db.ForeignKey("users.id"), primary_key=True),
    db.Column("flight_sessions", db.ForeignKey("flight_sessions.id"), primary_key=True),
)
