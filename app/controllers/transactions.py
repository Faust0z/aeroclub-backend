from flask import Blueprint, request
from app.models.balances import Balances
from app.services.balances import get_user_balance_srv
from app.services.transactions import obtenerTransacciones, obtener_transaccion

transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.get("/")
def get_transactions():
    try:
        transacciones = obtenerTransacciones()
        if transacciones:
            return {"response": transacciones}, 200
        else:
            return {"error": "ERROR"}, 404

    except Exception as ex:
        print(ex)
        return {"error": "ERROR"}, 401


@transactions_bp.get("/user/<str:email>")
def get_user_transactions_endp(email: str):
    try:
        # buscar la cuenta corriente asociada a ese usuario
        cuenta_corriente = get_user_balance_srv(email)

        if cuenta_corriente:
            # Usar el ID de la cuenta corriente para obtener las transacciones
            transacciones = obtener_transaccion(cuenta_corriente.id)

            if transacciones:
                return {"response": transacciones}, 200
            else:
                return {"error": "No se encontraron transacciones para este usuario"}, 404
        else:
            return {"error": "No se encontró la cuenta corriente para este usuario"}, 404
    except Exception as ex:
        print(ex)
        return {"error": "ERROR"}, 401


@transactions_bp.post("/")
def create_transaction_endp():
    try:
        data = request.get_json()
        monto = data.get("monto")
        idUsuario = data.get("idUsuario")
        motivo = data.get("motivo")
        tipoPago = data.get("tipoPago")
        fecha = data.get("fecha")
        idCuenta = get_user_balance_srv(idUsuario)

        if idCuenta:
            respuesta = update_balance_srv(idUsuario, monto, fecha, motivo, tipoPago)
            ## respuesta = transaccion_controller.crearTransaccion(monto, fecha, motivo,tipoPago,idCuentaCorriente)
            if respuesta:
                return {"message": "Transaccion created successfully"}, 201
            else:
                return {"error": "Some data is invalid"}, 400
        else:
            return {"error": "El usuario no posee una cuenta"}, 404
    except Exception as ex:
        print(ex)
        return {"error": "An error occurred"}, 401
