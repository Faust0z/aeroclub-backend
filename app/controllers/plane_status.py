from app.models.plane_status import PlaneStatus
from ..extensions import db


class EstadoAeronavesController:
    def __init__(self):
        pass

    def obtenerEstadosAeronaveById(self, id):
        estadoFound = PlaneStatus.query.get(id)
        if estadoFound:
            estadoSend = {
                "estado": estadoFound.estado,
            }
            return estadoSend
        return False

    def obtenerIdEstadoDeshabilitada(self):
        estadoAeroFound = (
            db.session.query(PlaneStatus).filter_by(estado="Deshabilitada").first()
        )

        if estadoAeroFound:
            estadoAeroFound = {
                "id": estadoAeroFound.id_estados_aeronaves,
            }
            return estadoAeroFound
        return False
