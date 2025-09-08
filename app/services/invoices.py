import math
from app.models.invoices import Invoices
from app.models.users import Users
from app.models.planes import Planes
from app.models.fares import Fares
from app.models.roles import Roles
from app.models.transactions import Transactions
from app.models.itineraries import Itineraries
from app.models.airport_codes import AirportCodes
from app.models.itinerary_types import ItineraryTypes
from .balances import update_balance_srv, rollback_payment_srv
from ..extensions import db
from datetime import datetime


# Business logic. Every 6 minutes → 0.1 h. Minutes can't exceed 60
def _calcularDecimalTablita(minutes: int) -> float:
    return min(math.ceil(minutes / 6) * 0.1, 1.0)


def _obtenerMayorTarifa(tarifas):
    if not tarifas: return None
    mayorTarifa = tarifas[0]
    for tarifa in tarifas:
        if tarifa.instruction_cost > mayorTarifa.instruction_cost:
            mayorTarifa = tarifa
    return mayorTarifa


def obtenerUnRecibo(numRecibo):
    try:
        recibo = db.session.query(Invoices).filter_by(numero_recibos=numRecibo).first()
        itinerarios = []
        if recibo:
            idRecibo = recibo.id
            print(f"id de cada recibo: {idRecibo}")
            instructor = aeronave = None
            instructorTieneRecibo = db.session.query(UsersHaveInvoices).filter_by(recibos_id=idRecibo, rol="Instructor").first()
            gestorTineneRecibo = db.session.query(UsersHaveInvoices).filter_by(recibos_id=idRecibo, rol="Gestor").first()
            asociadoTienenRecibo = db.session.query(UsersHaveInvoices).filter_by(recibos_id=idRecibo, rol="Asociado").first()
            if instructorTieneRecibo:
                instructor = db.session.query(Users).filter_by(id_usuarios=instructorTieneRecibo.user_id).first()
                print(f"Instructor name: {idRecibo} {instructor.first_name}")
            gestor = db.session.query(Users).filter_by(id_usuarios=gestorTineneRecibo.user_id).first()
            asociado = db.session.query(Users).filter_by(id_usuarios=asociadoTienenRecibo.user_id).first()
            transaccion = db.session.query(Transactions).filter_by(id_transacciones=recibo.transaction_id).first()
            getAllItinerarios = db.session.query(Itineraries).filter_by(RECIBOS_id_recibos=recibo.id).all()
            print(f"Gestor name:{idRecibo} {gestor.first_name}")
            for itinerario in getAllItinerarios:
                aeronave = db.session.query(Planes).filter_by(id_aeronaves=itinerario.plane_id).first()
                codsAeros = db.session.query(ItineraryHasAirportCodes).filter_by(itinerarios_id=itinerario.id).all()
                idCodAeroLlegada = codsAeros[0].codigos_aeropuertos_id
                idCodAeroSalida = codsAeros[1].codigos_aeropuertos_id
                codAeroLlegada = db.session.query(AirportCodes).filter_by(id_codigos_aeropuertos=idCodAeroLlegada).first()
                codAeroSalida = db.session.query(AirportCodes).filter_by(id_codigos_aeropuertos=idCodAeroSalida).first()
                tipoItinerario = db.session.query(ItineraryTypes).filter_by(
                    id_tipo_itinerarios=itinerario.itinerary_type_id).first()
                numero = str(itinerario.landings_amount) if type(
                    itinerario.landings_amount) == int else itinerario.landings_amount
                dictItinerario = {
                    "horaSalida": itinerario.departure_time,
                    "codAeroSalida": codAeroSalida.code,
                    "horaLlegada": itinerario.landing_time,
                    "codAeroLlegada": codAeroLlegada.code,
                    "cantAterrizajes": numero,
                    "tipoItinerario": tipoItinerario.name,
                }
                print(f"Un itinerario dict: {dictItinerario}")
                itinerarios.append(dictItinerario)
            if instructor:
                reciboCompleto = [{
                    "numRecibo": recibo.invoice_identifier,
                    "asociado": asociado.first_name + " " + asociado.last_name,
                    "instructor": instructor.nombre + " " + instructor.apellido,
                    "gestor": gestor.first_name + " " + gestor.last_name,
                    "precioTotal": transaccion.amount * (-1),
                    "observaciones": recibo.details,
                    "matricula": aeronave.matricula,
                }]
            else:
                reciboCompleto = [{
                    "numRecibo": recibo.invoice_identifier,
                    "asociado": asociado.first_name + " " + asociado.last_name,
                    "instructor": "",
                    "gestor": gestor.first_name + " " + gestor.last_name,
                    "precioTotal": transaccion.amount * (-1),
                    "observaciones": recibo.details,
                    "matricula": aeronave.matricula,
                }]
            reciboRetornar = reciboCompleto + itinerarios
            return reciboRetornar
        else:
            return False
    except Exception as ex:
        print(ex.args)
        return False


def obtenerRecibo(emailAsociado):
    try:
        recibos = []
        asociado = db.session.query(Users).filter_by(email=emailAsociado).first()
        if asociado:
            asociadoTinenRecibos = db.session.query(UsersHaveInvoices).filter_by(usuarios_id=asociado.id_usuarios,
                                                                                 rol="Asociado").all()
            print(asociadoTinenRecibos)
            for asociadoTieneRecibo in asociadoTinenRecibos:
                itinerarios = []
                idRecibo = asociadoTieneRecibo.recibos_id
                print(f"id de cada recibo: {idRecibo}")
                recibo = db.session.query(Invoices).filter_by(id_recibos=idRecibo).first()
                instructor = aeronave = None
                instructorTieneRecibo = db.session.query(UsersHaveInvoices).filter_by(recibos_id=idRecibo,
                                                                                      rol="Instructor").first()
                gestorTineneRecibo = db.session.query(UsersHaveInvoices).filter_by(recibos_id=idRecibo, rol="Gestor").first()
                if instructorTieneRecibo:
                    instructor = db.session.query(Users).filter_by(id_usuarios=instructorTieneRecibo.user_id).first()
                    print(f"Instructor name: {idRecibo} {instructor.first_name}")
                gestor = db.session.query(Users).filter_by(id_usuarios=gestorTineneRecibo.user_id).first()
                transaccion = db.session.query(Transactions).filter_by(id_transacciones=recibo.transaction_id).first()
                getAllItinerarios = db.session.query(Itineraries).filter_by(RECIBOS_id_recibos=recibo.id).all()
                print(f"Gestor name:{idRecibo} {gestor.first_name}")
                for itinerario in getAllItinerarios:
                    aeronave = db.session.query(Planes).filter_by(id_aeronaves=itinerario.plane_id).first()
                    codsAeros = db.session.query(ItineraryHasAirportCodes).filter_by(itinerarios_id=itinerario.id).all()
                    idCodAeroLlegada = codsAeros[0].codigos_aeropuertos_id
                    idCodAeroSalida = codsAeros[1].codigos_aeropuertos_id
                    codAeroLlegada = db.session.query(AirportCodes).filter_by(id_codigos_aeropuertos=idCodAeroLlegada).first()
                    codAeroSalida = db.session.query(AirportCodes).filter_by(id_codigos_aeropuertos=idCodAeroSalida).first()
                    tipoItinerario = db.session.query(ItineraryTypes).filter_by(
                        id_tipo_itinerarios=itinerario.itinerary_type_id).first()
                    numero = str(itinerario.landings_amount) if type(
                        itinerario.landings_amount) == int else itinerario.landings_amount
                    dictItinerario = {
                        "horaSalida": itinerario.departure_time,
                        "codAeroSalida": codAeroSalida.code,
                        "horaLlegada": itinerario.landing_time,
                        "codAeroLlegada": codAeroLlegada.code,
                        "cantAterrizajes": numero,
                        "tipoItinerario": tipoItinerario.name,
                    }
                    print(f"Un itinerario dict: {dictItinerario}")
                    itinerarios.append(dictItinerario)
                if instructor:
                    recibo_dict = [{
                        "numRecibo": recibo.invoice_identifier,
                        "asociado": asociado.first_name + " " + asociado.last_name,
                        "instructor": instructor.nombre + " " + instructor.apellido,
                        "gestor": gestor.first_name + " " + gestor.last_name,
                        "precioTotal": transaccion.amount * (-1),
                        "observaciones": recibo.details,
                        "matricula": aeronave.matricula,
                    }]
                else:
                    recibo_dict = [{
                        "numRecibo": recibo.invoice_identifier,
                        "asociado": asociado.first_name + " " + asociado.last_name,
                        "instructor": "",
                        "gestor": gestor.first_name + " " + gestor.last_name,
                        "precioTotal": transaccion.amount * (-1),
                        "observaciones": recibo.details,
                        "matricula": aeronave.matricula,
                    }]
                reciboCompleto = recibo_dict + itinerarios
                recibos.append(reciboCompleto)
            print(recibos)
            if recibos == []: return 2
            return recibos
        else:
            return 1
    except Exception as ex:
        print(ex.args)
        return "Ocurrió un error al obtener el recibo"


def crearRecibo(emailAsociado, emailInstructor, emailGestor, observaciones, matricula, fecha, itinerarios):
    try:
        transaccionInstructor = transaccionAsociado = None
        flagSiHayVuelosConInstructor = False
        aeronave = Planes.query.filter_by(matricula=matricula).first()
        asociado = db.session.query(Users).filter_by(email=emailAsociado).first()
        instructor = db.session.query(Users).filter_by(email=emailInstructor).first()
        gestor = db.session.query(Users).filter_by(email=emailGestor).first()
        rolAsociado = db.session.query(Roles).filter_by(tipo="Asociado").first()
        asociadoTieneRol = db.session.query(UsersHaveRoles).filter_by(usuarios_id=asociado.id_usuarios,
                                                                      roles_id=rolAsociado.id).first()
        rolGestor = db.session.query(Roles).filter_by(tipo="Gestor").first()
        gestorTieneRol = db.session.query(UsersHaveRoles).filter_by(usuarios_id=gestor.id_usuarios, roles_id=rolGestor.id).first()
        if not (asociadoTieneRol): return 1
        if not (gestorTieneRol): return 2
        if aeronave:
            tarifa = Fares.query.filter_by(aeronaves_id=aeronave.id_aeronaves).first()
            tarifasTotales = Fares.query.all()
            tarifaInstructor = _obtenerMayorTarifa(tarifasTotales)
            print(f"Esta es la tarifa mas cara: {tarifaInstructor}")
            precioItinerarios = []
            for itinerario in itinerarios:
                print(f"itinerario: {itinerario}")
                salida = datetime.strptime(itinerario.get("horaSalida"), "%Y-%m-%d %H:%M:%S")
                llegada = datetime.strptime(itinerario.get("horaLlegada"), "%Y-%m-%d %H:%M:%S")
                diferencia = -(salida - llegada)
                diferencia_en_horas = diferencia.total_seconds() / 3600
                horas_fraccionaria, horas = math.modf(diferencia_en_horas)
                if horas_fraccionaria:
                    minutos = horas_fraccionaria * 60
                    horas = horas + _calcularDecimalTablita(minutos)
                if (itinerario.get("tipoItinerario") == "Sólo con instrucción") | (
                        itinerario.get("tipoItinerario") == "Doble comando"):
                    print(f"tarifa: {tarifa}")
                    precioCadaItinerario = {
                        "vuelo": tarifa.fare_value * horas,
                        "instuccion": tarifaInstructor.importe_instruccion * horas,
                    }
                    precioItinerarios.append(precioCadaItinerario)
                    if instructor:
                        rolInstructor = db.session.query(Roles).filter_by(tipo="Instructor").first()
                        instructorTieneRol = db.session.query(UsersHaveRoles).filter_by(usuarios_id=instructor.id_usuarios,
                                                                                        roles_id=rolInstructor.id).first()
                        if instructorTieneRol:
                            flagSiHayVuelosConInstructor = True
                        else:
                            return 3
                    else:
                        return 4
                else:
                    precioCadaItinerario = {
                        "vuelo": tarifa.fare_value * horas,
                        "instuccion": 0,
                    }
                    precioItinerarios.append(precioCadaItinerario)
            fecha_actual = datetime.now()
            fecha = f"{fecha_actual.year}-{fecha_actual.month}-{fecha_actual.day}"
            precioTotalVuelo = valorPagoInstructor = 0
            for precioPorItinerario in precioItinerarios:
                if precioPorItinerario.get("instuccion") > 0:
                    valorPagoInstructor += precioPorItinerario.get("instuccion")
                precioTotalVuelo += precioPorItinerario.get("vuelo") + precioPorItinerario.get("instuccion")
            precioTotalVuelo *= -1
            update_balance_srv(asociado.id_usuarios, precioTotalVuelo, fecha, "Pago de vuelo", "Efectivo")
            if transaccionAsociado:
                tipoRecibo = db.session.query(ReceiptTypes).filter_by(tipo="Recibo de Vuelo").first()
                num_recibo = 0
                reciboMayor = db.session.query(Invoices).order_by(Invoices.invoice_identifier.desc()).first()
                if reciboMayor: num_recibo = reciboMayor.invoice_identifier + 1
                recibo = Invoices(
                    None, fecha_actual, observaciones, tipoRecibo.id,
                    transaccionAsociado.id_transacciones, num_recibo
                )
                if instructor:
                    update_balance_srv(instructor.id_usuarios, valorPagoInstructor, fecha, "Pago de vuelo", "Efectivo")
                if recibo:
                    db.session.add(recibo)
                    db.session.commit()
                    print(f"este es el recibo id: {recibo.id}")
                    asociadoTieneRecibo = UsersHaveInvoices(None, recibo.id, asociado.id_usuarios, "Asociado")
                    gestorTieneRecibo = UsersHaveInvoices(None, recibo.id, gestor.id_usuarios, "Gestor")
                    db.session.add(asociadoTieneRecibo)
                    db.session.add(gestorTieneRecibo)
                    db.session.commit()
                    if instructor and flagSiHayVuelosConInstructor:
                        instructorTieneRecibo = UsersHaveInvoices(None, recibo.id, instructor.id_usuarios, "Instructor")
                        db.session.add(instructorTieneRecibo)
                        db.session.commit()
                    itinerariosCreadosConSuRelacion = []
                    for itinerario in itinerarios:
                        print(f"este es el itinerario : {itinerario}")
                        respuestaCreacionItinerario = crearItinerario(
                            itinerario.get("horaSalida"),
                            itinerario.get("codAeroSalida"),
                            itinerario.get("horaLlegada"),
                            itinerario.get("codAeroLlegada"),
                            observaciones,
                            itinerario.get("cantAterrizajes"),
                            matricula,
                            itinerario.get("tipoItinerario"),
                            recibo.id,
                        )
                        itinerariosCreadosConSuRelacion.append(respuestaCreacionItinerario)
                    if not respuestaCreacionItinerario[0]:
                        print("no se cargo algun itinerario")
                        print(f"ENTRE a la excepcion, asociado: {asociado}")
                        if instructor and transaccionInstructor:
                            montoInstructor = transaccionInstructor.monto
                            idCuentaCorrienteInstructor = transaccionInstructor.cuenta_corriente_id
                            db.session.delete(transaccionInstructor)
                            resDos = rollback_payment_srv(montoInstructor, idCuentaCorrienteInstructor)
                            print(f"se retrotrajo el pago del instructor: {resDos} ")
                        if asociado and transaccionAsociado:
                            montoAsociado = transaccionAsociado.amount
                            idCuentaCorrienteAsociado = transaccionAsociado.balance_id
                            db.session.delete(transaccionAsociado)
                            resUno = rollback_payment_srv(montoAsociado, idCuentaCorrienteAsociado)
                            print(f"se retrotrajo el pago del asociado: {resUno} ")
                        db.session.commit()
                        return 5
                    return [13, recibo.invoice_identifier]
                else:
                    return 6
            else:
                return 7
        else:
            return 9
    except Exception as ex:
        print(ex)
        print(f"ENTRE a la excepcion, asociado: {asociado}")
        if instructor and transaccionInstructor:
            montoInstructor = transaccionInstructor.monto
            idCuentaCorrienteInstructor = transaccionInstructor.cuenta_corriente_id
            db.session.delete(transaccionInstructor)
            resDos = rollback_payment_srv(montoInstructor, idCuentaCorrienteInstructor)
            print(f"se retrotrajo el pago del instructor: {resDos} ")
        if asociado and transaccionAsociado:
            montoAsociado = transaccionAsociado.monto
            idCuentaCorrienteAsociado = transaccionAsociado.cuenta_corriente_id
            db.session.delete(transaccionAsociado)
            resUno = rollback_payment_srv(montoAsociado, idCuentaCorrienteAsociado)
            print(f"se retrotrajo el pago del asociado: {resUno} ")
            db.session.commit()
        else:
            return 10
        if not gestor:
            return 11
        db.session.commit()
        return 8


def obtenerTodosLosRecibos():
    try:
        todosLosRecibos = []
        tipoRecibo = db.session.query(ReceiptTypes).filter_by(tipo="Recibo de Vuelo").first()
        recibos = db.session.query(Invoices).filter_by(tipo_recibos_id=tipoRecibo.id).all()
        for recibo in recibos:
            itinerarios = []
            instructor = aeronave = None
            asociadoTieneRecibo = db.session.query(UsersHaveInvoices).filter_by(recibos_id=recibo.id, rol="Asociado").first()
            instructorTieneRecibo = db.session.query(UsersHaveInvoices).filter_by(recibos_id=recibo.id, rol="Instructor").first()
            gestorTineneRecibo = db.session.query(UsersHaveInvoices).filter_by(recibos_id=recibo.id, rol="Gestor").first()
            if instructorTieneRecibo:
                instructor = db.session.query(Users).filter_by(id_usuarios=instructorTieneRecibo.user_id).first()
            gestor = db.session.query(Users).filter_by(id_usuarios=gestorTineneRecibo.user_id).first()
            asociado = db.session.query(Users).filter_by(id_usuarios=asociadoTieneRecibo.user_id).first()
            transaccion = db.session.query(Transactions).filter_by(id_transacciones=recibo.transaction_id).first()
            getAllItinerarios = db.session.query(Itineraries).filter_by(RECIBOS_id_recibos=recibo.id).all()
            for itinerario in getAllItinerarios:
                aeronave = db.session.query(Planes).filter_by(id_aeronaves=itinerario.plane_id).first()
                codsAeros = db.session.query(ItineraryHasAirportCodes).filter_by(itinerarios_id=itinerario.id).all()
                idCodAeroLlegada = codsAeros[0].codigos_aeropuertos_id
                idCodAeroSalida = codsAeros[1].codigos_aeropuertos_id
                codAeroLlegada = db.session.query(AirportCodes).filter_by(id_codigos_aeropuertos=idCodAeroLlegada).first()
                codAeroSalida = db.session.query(AirportCodes).filter_by(id_codigos_aeropuertos=idCodAeroSalida).first()
                tipoItinerario = db.session.query(ItineraryTypes).filter_by(
                    id_tipo_itinerarios=itinerario.itinerary_type_id).first()
                numero = str(itinerario.landings_amount) if type(
                    itinerario.landings_amount) == int else itinerario.landings_amount
                dictItinerario = {
                    "horaSalida": itinerario.departure_time,
                    "codAeroSalida": codAeroSalida.code,
                    "horaLlegada": itinerario.landing_time,
                    "codAeroLlegada": codAeroLlegada.code,
                    "cantAterrizajes": numero,
                    "tipoItinerario": tipoItinerario.name,
                }
                print(f"Un itinerario dict: {dictItinerario}")
                itinerarios.append(dictItinerario)
            if instructor:
                devolverRecibo = [{
                    "numRecibo": recibo.invoice_identifier,
                    "asociado": asociado.first_name + " " + asociado.last_name,
                    "instructor": instructor.nombre + " " + instructor.apellido,
                    "gestor": gestor.first_name + " " + gestor.last_name,
                    "precioTotal": transaccion.amount * (-1),
                    "observaciones": recibo.details,
                    "matricula": aeronave.matricula,
                }]
            else:
                devolverRecibo = [{
                    "numRecibo": recibo.invoice_identifier,
                    "asociado": asociado.first_name + " " + asociado.last_name,
                    "instructor": "",
                    "gestor": gestor.first_name + " " + gestor.last_name,
                    "precioTotal": transaccion.amount * (-1),
                    "observaciones": recibo.details,
                    "matricula": aeronave.matricula,
                }]
            reciboCompleto = devolverRecibo + itinerarios
            todosLosRecibos.append(reciboCompleto)
        if recibos == []: return 1
        return todosLosRecibos
    except Exception as ex:
        print(ex.args)
        return "Ocurrió un error al obtener el recibo"
