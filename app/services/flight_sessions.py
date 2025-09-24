import math
from datetime import date, datetime, UTC

from sqlalchemy.orm import joinedload

from app.models import FlightSessions, Itineraries, Planes, Users, Transactions
from .airport_codes import get_airport_code_by_code_srv
from .payment_types import get_payment_type_by_name_srv
from .planes import get_plane_by_registration_srv
from .transactions import sub_user_transaction_srv
from .users import get_user_by_email_srv
from ..errors import UserNotFound, PlaneFareNotFound, BadTimeInput, FlightSessionNotFound
from ..extensions import db


def get_flight_sessions_srv(flight_session_identifier: int | None = None, plane_registration: str | None = None,
                            admin_email: str | None = None, user_first_name: str | None = None, user_last_name: str | None = None,
                            observations: str | None = None,
                            starting_date: date | None = None, limit_date: date | None = None) -> list[FlightSessions]:
    stmt = db.select(FlightSessions)

    if flight_session_identifier:
        stmt = stmt.where(FlightSessions.flight_session_identifier == flight_session_identifier)
    if admin_email or user_first_name or user_last_name:
        stmt = stmt.join(FlightSessions.users)
        if admin_email:
            stmt = stmt.where(Users.email.ilike(f"%{admin_email}%"))
        if user_first_name:
            stmt = stmt.where(Users.first_name.ilike(f"%{user_first_name}%"))
        if user_last_name:
            stmt = stmt.where(Users.last_name.ilike(f"%{user_last_name}%"))
    if plane_registration:
        stmt = stmt.join(FlightSessions.itinerary).join(Itineraries.plane)
        stmt = stmt.where(Planes.registration.ilike(f"%{plane_registration}%"))
    if starting_date and limit_date:
        stmt = stmt.where(db.and_(FlightSessions.issued_date >= starting_date, FlightSessions.issued_date <= limit_date))
    elif starting_date:
        stmt = stmt.where(FlightSessions.issued_date >= starting_date)
    elif limit_date:
        stmt = stmt.where(FlightSessions.issued_date <= limit_date)
    if observations:
        stmt = stmt.where(FlightSessions.observations.ilike(f"%{observations}%"))

    return db.session.execute(stmt).unique().scalars().all()


# This method does not use the get_user_by_email_srv method as the rest in order to eager load the flight_sessions
def get_user_flight_sessions_srv(email: str) -> list[FlightSessions]:
    user = db.session.scalar_one_or_none(
        db.select(Users)
        .options(
            joinedload(Users.flight_sessions).joinedload(FlightSessions.itinerary).joinedload(Itineraries.plane),
            joinedload(Users.flight_sessions).joinedload(FlightSessions.itinerary).joinedload(Itineraries.airport_codes),
            joinedload(Users.flight_sessions).joinedload(FlightSessions.users)
        )
        .where(Users.email == email)
    )
    if not user:
        raise UserNotFound
    return user.flight_sessions


# This method does not use the get_user_by_email_srv method as the rest in order to eager load the flight_sessions
def get_flight_session_by_identifier_srv(flight_session_identifier: int) -> FlightSessions:
    flight_session = db.session.scalar_one_or_none(
        db.select(FlightSessions)
        .options(
            joinedload(FlightSessions.itinerary).joinedload(Itineraries.plane),
            joinedload(FlightSessions.itinerary).joinedload(Itineraries.airport_codes),
            joinedload(FlightSessions.users)
        )
        .where(FlightSessions.flight_session_identifier == flight_session_identifier)
    )
    if not flight_session:
        raise FlightSessionNotFound
    return flight_session


def create_flight_session_srv(flight_session: FlightSessions, user_email: str, instructor_email: str | None,
                              admin_email: str) -> FlightSessions:
    last_identifier = db.session.query(db.func.max(FlightSessions.flight_session_identifier)).scalar()
    next_identifier = (last_identifier or 0) + 1
    # Creates a local instance to make sure that all the data is in a single session
    new_flight_session = FlightSessions(
        flight_session_identifier=next_identifier,
        issued_date=flight_session.issued_date,
        observations=flight_session.observations,
    )

    admin = get_user_by_email_srv(email=admin_email)
    user = get_user_by_email_srv(email=user_email)
    if instructor_email:
        instructor = get_user_by_email_srv(email=instructor_email)
        new_flight_session.users.append(instructor)
    new_flight_session.users.append(user)
    new_flight_session.users.append(admin)

    total_session_cost = 0
    for itinerary in flight_session.itineraries:
        new_itinerary, itinerary_cost = __build_itinerary(itinerary)
        new_flight_session.itineraries.append(new_itinerary)
        total_session_cost += itinerary_cost

    try:
        new_transaction = sub_user_transaction_srv(
            email=user_email,
            transaction=Transactions(
                amount=total_session_cost,
                issued_date=datetime.now(UTC),
                description="Transaction automatically created by flight session",
                payment_type_id=get_payment_type_by_name_srv("Flight Session"),
                balance_id=user.balance.id
            )
        )

        new_flight_session.transaction_id = new_transaction.id
        db.session.add(new_flight_session)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return new_flight_session


def __calculate_itinerary_cost(itinerary: Itineraries, plane: Planes) -> float:
    if itinerary.departure_time >= itinerary.arrival_time:
        raise BadTimeInput

    diff_hours = (itinerary.arrival_time - itinerary.departure_time).total_seconds() / 3600
    minutes_fraction, whole_hours = math.modf(diff_hours)
    cost = whole_hours

    # Business logic. Every 6 minutes → 0.1 h. Minutes can't exceed 60
    cost += min(math.ceil((minutes_fraction * 60) / 6) * 0.1, 1.0)

    return cost * plane.fare.amount


def __build_itinerary(itinerary: Itineraries) -> tuple[Itineraries, float]:
    plane = get_plane_by_registration_srv(itinerary.plane.registration)
    if not plane.fare:
        raise PlaneFareNotFound

    new_itinerary = Itineraries(
        departure_time=itinerary.departure_time,
        arrival_time=itinerary.arrival_time,
        landings_amount=itinerary.landings_amount,
        observations=itinerary.observations,
        itinerary_type_id=itinerary.itinerary_type_id,
        plane=plane
    )

    for airport_code in itinerary.airport_codes:
        db_airport = get_airport_code_by_code_srv(code=airport_code.code)
        new_itinerary.airport_codes.append(db_airport)

    return new_itinerary, __calculate_itinerary_cost(itinerary, plane)
