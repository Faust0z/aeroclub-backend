from app.models.transactions import Transactions
from app.models.payment_types import PaymentTypes
from app.models.balances import Balances
from app.models.users import Users
from app.models.payment_types import PaymentTypes
from ..extensions import db


class TransaccionesController:
    def _init_(self):
        pass

    def __chequearTipoPago(self, tipoPago):
        tipos = ["Cheque", "Efectivo", "Transferencia"]
        print(f"__chequearTipoPago tipoPago entro: {tipoPago}")
        resultado = [x for x in tipos if x == tipoPago]

        if resultado:
            return True
        else:
            return False

    def crearTransaccion(self, monto, fecha, motivo, tipoPago, idCuentaCorriente):
        try:
            # chequeando el tipo de pago
            if self.__chequearTipoPago(self.__chequearTipoPago, tipoPago):
                # aca me traigo el tipoPago para obtener su id
                tipoPagoDictionary = db.session.query(PaymentTypes).filter_by(tipo=tipoPago).first()

                transaccion = Transactions(None, monto, fecha, motivo, tipoPagoDictionary.id, idCuentaCorriente)

                db.session.add(transaccion)
                db.session.commit()

                return transaccion

            else:
                return False
        except Exception as ex:
            print(ex)
            return False

    def obtenerTransacciones(self):
        try:
            transacciones = Transactions.query.all()
            transaccion_list = []

            for transaccion in transacciones:
                idCuentaCorriente = transaccion.balance_id
                cuentaCorriente = db.session.query(Balances).filter_by(id_cuenta_corriente=idCuentaCorriente).first()
                usuario = db.session.query(Users).filter_by(id_usuarios=cuentaCorriente.user_id).first()
                tipoPago = db.session.query(PaymentTypes).filter_by(id_tipo_pago=transaccion.fare_type_id).first()
                transaccion_data = {
                    'id_transacciones': transaccion.id_transacciones,
                    'nombre_completo_usuario': usuario.first_name + " " + usuario.last_name,
                    'monto': transaccion.amount,
                    'fecha': transaccion.issued_date,
                    'motivo': transaccion.description,
                    'tipo_pago_id': tipoPago.name,
                    'cuenta_corriente_id': transaccion.balance_id,
                }
                transaccion_list.append(transaccion_data)
            return transaccion_list

        except Exception as ex:
            print(ex)
            return False

    # Obtener todas las transacciones de un usuario según su id
    def obtener_transaccion(self, cuenta_corriente_id):
        transaccion_uid = Transactions.query.filter_by(cuenta_corriente_id=cuenta_corriente_id)
        transaccion_uid_list = []

        for transaccion in transaccion_uid:
            transaccion_data = {
                'id_transacciones': transaccion.id_transacciones,
                'monto': transaccion.amount,
                'fecha': transaccion.issued_date,
                'motivo': transaccion.description,
                'tipo_pago_id': transaccion.fare_type_id,
                'cuenta_corriente_id': transaccion.balance_id,
            }
            transaccion_uid_list.append(transaccion_data)
        return transaccion_uid_list
