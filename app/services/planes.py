from app.models.planes import Planes
from ..extensions import db


def obtenerAeronavePorMatricula(matricula):
    try:
        aeronave = Planes.query.filter_by(matricula=matricula).first()

        if aeronave:
            estadoFound = obtenerEstadosAeronaveById(aeronave.estados_aeronaves_id)
            aeronave_data = {
                "marca": aeronave.marca,
                "modelo": aeronave.modelo,
                "matricula": aeronave.matricula,
                "potencia": aeronave.potencia,
                "clase": aeronave.clase,
                "fecha_adquisicion": aeronave.fecha_adquisicion,
                "consumo_por_hora": aeronave.consumo_por_hora,
                "path_documentacion": aeronave.path_documentacion,
                "descripcion": aeronave.descripcion,
                "path_imagen_aeronave": aeronave.path_imagen_aeronave,
                "estados": estadoFound.get("estado"),
            }
            return aeronave_data
        else:
            return False
    except Exception as ex:
        print(ex.args)
        return False


def obtenerAeronaves():
    idDeshabilitado = obtenerIdEstadoDeshabilitada()

    aeronaves = Planes.query.filter(Planes.estados_aeronaves_id != idDeshabilitado.get("id")).all()
    aeronave_list = []

    for aeronave in aeronaves:
        aeronave_data = {
            "id_aeronaves": aeronave.id_aeronaves,
            "marca": aeronave.marca,
            "modelo": aeronave.modelo,
            "matricula": aeronave.matricula,
            "potencia": aeronave.potencia,
            "clase": aeronave.clase,
            "fecha_adquisicion": aeronave.fecha_adquisicion,
            "consumo_por_hora": aeronave.consumo_por_hora,
            "path_documentacion": aeronave.path_documentacion,
            "descripcion": aeronave.descripcion,
            "path_imagen_aeronave": aeronave.path_imagen_aeronave,
            "estados_aeronaves_id": aeronave.estados_aeronaves_id,
        }
        aeronave_list.append(aeronave_data)
    return aeronave_list


# al estar cargada no lo modificamos asi que no funciona como deberia en la db completa
def crearAeronave(data):
    aeronave = Planes(**data)
    db.session.add(aeronave)
    db.session.commit()
    return True


def editarAeronave(matricula, data):
    aeronave = Planes.query.filter_by(matricula=matricula).first()
    if aeronave:
        for key, value in data.items():
            setattr(aeronave, key, value)
        db.session.commit()
        return True
    return False


def disable_plane(matricula):
    aeronave = Planes.query.filter_by(matricula=matricula).first()
    idDeshabilitado = obtenerIdEstadoDeshabilitada()

    if aeronave:
        aeronave.estados_aeronaves_id = idDeshabilitado.get("id")
        db.session.commit()
        return True
    return False
