from flask import Blueprint
from app.services.balances import get_user_balance_srv

balances_bp = Blueprint("balances", __name__, url_prefix='/balances')


@balances_bp.get("/<string:email>")
def get_balance_endp(email: int):
    try:
        saldo = get_user_balance_srv(email)

        if saldo:
            return {"saldo_cuenta": saldo}, 200
        else:
            return {"error": "Cuenta corriente no encontrada para este usuario"}, 404
    except Exception as ex:
        print(ex)
        return {"error": "ERROR"}, 401
