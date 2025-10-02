from sqlalchemy.exc import IntegrityError

from app.models.plane_status import PlaneStatus
from ..errors import PlaneStatusAlreadyExists, PlaneStatusNotFound
from ..extensions import db


def get_planes_status_srv() -> list[PlaneStatus]:
    return db.session.scalars(db.select(PlaneStatus)).all()


def get_plane_status_by_name_srv(name: str) -> PlaneStatus:
    plane_status = db.session.execute(db.select(PlaneStatus).where(PlaneStatus.state == name)).scalar_one_or_none()
    if not plane_status:
        raise PlaneStatusNotFound
    return plane_status


def update_plane_status_srv(name: str, data: dict) -> PlaneStatus:
    plane_status = get_plane_status_by_name_srv(name=name)
    try:
        for key, value in data.items():
            if hasattr(plane_status, key):
                setattr(plane_status, key, value)
        db.session.commit()
    except IntegrityError:
        raise PlaneStatusAlreadyExists

    return plane_status
