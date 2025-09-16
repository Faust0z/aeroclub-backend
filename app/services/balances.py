from app.models.balances import Balances
from .transactions import crearTransaccion
from ..extensions import db


def get_user_balance_srv(idAsociado):
    try:
        cuantaCorrienteAsociado = Balances.query.filter_by(usuarios_id=idAsociado).first()
        if cuantaCorrienteAsociado:
            return cuantaCorrienteAsociado.id
        else:
            return False
    except Exception as ex:
        print(ex)
        return False


def update_balance_srv(usuario_id, monto, fecha, motivo, tipoPago):
    cuenta_corriente = Balances.query.filter_by(
        usuarios_id=usuario_id
    ).first()

    transaccion = crearTransaccion(
        monto,
        fecha,
        motivo,
        tipoPago,
        cuenta_corriente.id,
    )
    print(f"transaccion: {transaccion}")
    if (cuenta_corriente) and (transaccion):
        print(f"transaccion: {transaccion.amount}")
        cuenta_corriente.balance = (cuenta_corriente.balance + transaccion.amount)
        db.session.commit()
        return transaccion
    return False


# TODO: check if this is a necessary method, or if it's possible to manage with SQLA sessions
def rollback_payment_srv(monto, id):
    cuenta_corriente = (
        db.session.query(Balances).filter_by(usuarios_id=id).first()
    )
    monto = monto * (-1)
    print(f"monto: {monto}")
    print(f"cuenta corriente: {cuenta_corriente.balance}")
    if cuenta_corriente:
        cuenta_corriente.balance = cuenta_corriente.balance + monto
        print(f"nuevo saldo: {cuenta_corriente.balance}")
        db.session.commit()
        return True
    return False


# A balance can't be deleted, only disabled
def disable_account_srv():
    pass
