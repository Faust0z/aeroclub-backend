from app.models.balances import Balances
from app.controllers.transactions import TransaccionesController
from ..extensions import db


class cuentaCorrienteController:  # Delete this class stuff
    def _init_(self):
        pass

    def crear_cuenta(self, idUsuario):
        cuentaCorriente = Balances(0, 0, idUsuario)
        db.session.add(cuentaCorriente)
        db.session.commit()

    def obtenerCuentaCorriente(self, idAsociado):
        try:
            cuantaCorrienteAsociado = Balances.query.filter_by(
                usuarios_id=idAsociado
            ).first()
            if cuantaCorrienteAsociado:
                return cuantaCorrienteAsociado.id
            else:
                return False
        except Exception as ex:
            print(ex)
            return False

    def obtener_saldo(self, usuario_id):
        cuenta_corriente = Balances.query.filter_by(
            usuarios_id=usuario_id
        ).first()
        if cuenta_corriente:
            return cuenta_corriente.balance, True
        return False

    def actualizar_saldo(self, usuario_id, monto, fecha, motivo, tipoPago):
        cuenta_corriente = Balances.query.filter_by(
            usuarios_id=usuario_id
        ).first()

        transaccion = TransaccionesController.crearTransaccion(
            TransaccionesController,
            monto,
            fecha,
            motivo,
            tipoPago,
            cuenta_corriente.id,
        )
        print(f"transaccion: {transaccion}")
        if (cuenta_corriente) and (transaccion):
            print(f"transaccion: {transaccion.amount}")
            cuenta_corriente.balance = (
                    cuenta_corriente.balance + transaccion.amount
            )
            db.session.commit()
            return transaccion
        return False

    def retrotraer_pago(self, monto, id):
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
    def delete_account(self):
        pass
