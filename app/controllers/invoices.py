from flask import Blueprint, request

from app.services.invoices import obtenerTodosLosRecibos, obtenerRecibo, crearRecibo

invoices_bp = Blueprint("invoices", __name__, url_prefix='/invoices')


@invoices_bp.get("/")
def get_invoices_endp():
    try:
        respuesta = obtenerTodosLosRecibos()
        if respuesta == 1:
            return {
                "error": "No hay recibos de vuelos"
            }, 404
        if respuesta:
            return {"respuesta": respuesta}, 200
    except Exception as ex:
        print(ex)
        return {"error": "ocurrio un error"}, 401


@invoices_bp.get("/<string:email>")
def get_user_invoices_endp(email: str):
    try:
        respuesta = obtenerRecibo(email)
        if respuesta == 1:
            return {"error": "El mail no le pertenece a un asociado"}, 404
        if respuesta == 2:
            return {"error": "El asociado no tiene recibos aún"}, 404
        if respuesta:
            return {"respuesta": respuesta}, 200
    except Exception as ex:
        print(ex)
        return {"error": "ocurrio un error"}, 401


@invoices_bp.post("/")
def create_invoice_endp():
    try:
        data = request.get_json()
        emailAsociado = data.get("emailAsociado")
        emailInstructor = data.get("emailInstructor")
        emailGestor = data.get("emailGestor")
        observaciones = data.get("observaciones")
        matricula = data.get("matricula")
        fecha = data.get("fecha")
        itinerarios = data.get("itinerarios")
        respuesta = crearRecibo(
            emailAsociado,
            emailInstructor,
            emailGestor,
            observaciones,
            matricula,
            fecha,
            itinerarios,
        )

        if respuesta == 1:
            return {
                "error": "El asociado que ingreso, no tiene rol de Asociado"
            }, 400
        if respuesta == 2:
            return {
                "error": "El gestor que ingreso, no tiene rol de Gestor"
            }, 400
        if respuesta == 3:
            return {
                "error": "El instructor que ingreso, no tiene rol de instrunctor"
            }, 400
        if respuesta == 4:
            return {
                "error": "El instructor no es valido"
            }, 400
        if respuesta == 5:
            return {
                "error": "Algún itinerario tiene un dato erroneo"
            }, 400
        if respuesta == 6:
            return {
                "error": "Algun dato del Recibo esta erroneo"
            }, 400
        if respuesta == 7:
            return {
                "error": "Hubo un error en la transacción verifique los dato y envie nuevamente"
            }, 400
        if respuesta == 8:
            return {
                "error": "Algún dato de los itinerarios es erroneo, veifique los dato y envie nuevamente"
            }, 400
        if respuesta == 9:
            return {
                "error": "La aeronave no es válida, ingrese una matrícula válida"
            }, 400
        if respuesta == 10:
            return {
                "error": "El Asociado no es un usuario válido"
            }, 400
        if respuesta == 11:
            return {
                "error": "El Gestor no es un usuario válido"
            }, 400

    except Exception as ex:
        print(ex.args)
        return {"error": "error"}, 401


"""
@reciboVuelos_bp.delete('/transaccion')
def eliminarTransaccion():
  
    has_access = Security.verify_token(request.headers)
    
    if has_access:
        try:
                data = request.get_json()
                id=data.get("id")
                
                transaccionesController = TransaccionesController()
                respuesta = transaccionesController.eliminarTransaccion(id)
                if respuesta :
                    return jsonify({"respuesta":respuesta})
                else:
                    return jsonify({"respuesta":False})
        except Exception as ex:
            print(ex)
            return jsonify({'message': 'ocurrio un error', 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
"""
