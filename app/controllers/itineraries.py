from app.models.itineraries import Itineraries
from app.models.associations import ItineraryHasAirportCodes
from app.models.itineraries import AirportCodes
from app.models.itinerary_types import ItineraryTypes
from app.models.planes import Planes
from sqlalchemy.orm import joinedload
from ..extensions import db


class ItinerariosController:

    def __init__(self):
        pass

    def __chequearTipoItinerario(tipoItinerario):

        tipos = [
            "Sólo con instrucción",
            "Doble comando",
            "Travesía",
            "Vuelo por Instrumentos bajo capota",
            "Vuelo nocturno",
        ]

        resultado = [x for x in tipos if x == tipoItinerario]
        if resultado:
            return True
        else:
            return False

    def __chequearCodigosAeropuertos(codAeroLlegada, codAeroSalida):
        tipos = ["LIN", "AER1", "AER2", "AER3", "AER4"]
        resultadoUno = [x for x in tipos if x == codAeroLlegada]
        resultadoDos = [x for x in tipos if x == codAeroSalida]

        if resultadoUno and resultadoDos:
            return True
        else:
            return False

    def crearItinerario(
            self,
            horaSalida,
            codAeroSalida,
            horaLlegada,
            codAeroLlegada,
            observaciones,
            cantAterrizajes,
            matricula,
            tipoItinerario,
            idRecibo,
    ):
        try:
            # chequeando el tipo de itinerario y los codigos del aeropuerto
            if self.__chequearTipoItinerario(
                    tipoItinerario
            ) & self.__chequearCodigosAeropuertos(codAeroLlegada, codAeroSalida):
                # aca me traigo el tipoItinerario para obtener su id
                tipoItinerario = (
                    db.session.query(ItineraryTypes)
                    .filter_by(tipo=tipoItinerario)
                    .first()
                )
                # aca me traigo un codigo aeropuerto para obtener su id
                codigosAeropuertosLlegada = (
                    db.session.query(AirportCodes)
                    .filter_by(codigo_aeropuerto=codAeroLlegada)
                    .first()
                )
                # aca me traigo un codigo aeropuerto para obtener su id
                codigosAeropuertosSalida = (
                    db.session.query(AirportCodes)
                    .filter_by(codigo_aeropuerto=codAeroSalida)
                    .first()
                )
                # aca me traigo la aeronave para obtener el id
                aeronave = (
                    db.session.query(Planes).filter_by(matricula=matricula).first()
                )
                # creo el itinerario
                itinerario = Itineraries(
                    None,
                    horaSalida,
                    horaLlegada,
                    cantAterrizajes,
                    observaciones,
                    tipoItinerario.id_tipo_itinerarios,
                    aeronave.id_aeronaves,
                    idRecibo,
                )
                db.session.add(itinerario)
                db.session.commit()

                itinerarioTieneCodigosAeropuertosUno = (
                    ItineraryHasAirportCodes(
                        None,
                        itinerario.id_itinerarios,
                        codigosAeropuertosLlegada.id_codigos_aeropuertos,
                    )
                )

                db.session.add(itinerarioTieneCodigosAeropuertosUno)
                db.session.commit()

                itinerarioTieneCodigosAeropuertosDos = (
                    ItineraryHasAirportCodes(
                        None,
                        itinerario.id_itinerarios,
                        codigosAeropuertosSalida.id_codigos_aeropuertos,
                    )
                )

                db.session.add(itinerarioTieneCodigosAeropuertosDos)
                db.session.commit()

                return [
                    itinerario,
                    itinerarioTieneCodigosAeropuertosUno,
                    itinerarioTieneCodigosAeropuertosDos,
                ]

            else:
                return 1
        except Exception as ex:
            print(ex)
            return 3
