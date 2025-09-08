from flask import Blueprint, request

from app.services.planes import obtenerAeronaves, crearAeronave, editarAeronave, disable_plane

planes_bp = Blueprint('planes', __name__)


@planes_bp.get('/')
def get_planes_endp():
    try:
        aeronaves = obtenerAeronaves()
        if aeronaves:
            return {'respuesta': aeronaves}, 200
        else:
            return {'error': 'No se encontraron las aeronaves'}, 404
    except Exception as ex:
        print(ex)
        return {'error': 'ERROR'}, 401


@planes_bp.get('/<str:registration>')
def get_plane_endp(registration: str):
    try:
        aeronave = obtenerAeronavePorMatricula(registration)

        if aeronave:
            return {'respuesta': aeronave}, 200
        else:
            return {'error': 'No se encontro la aeronave'}, 404
    except Exception as ex:
        print(ex)
        return {'error': 'ERROR'}, 401


@planes_bp.post('/')
def create_plane_endp():
    try:
        data = request.get_json()
        respuesta = crearAeronave(data)
        if respuesta:
            return {'message': 'Aeronave created successfully'}, 201
        else:
            return {'error': 'Some data is invalid'}, 400
    except Exception as ex:
        print(ex)
        return {'error': 'An error occurred'}, 401


@planes_bp.patch('/<str:registration>')
def update_plane(registration: str):
    try:
        data = request.get_json()
        respuesta = editarAeronave(registration, data)
        if respuesta:
            return {'message': 'Aeronave updated successfully'}, 200
        else:
            return {'error': 'Aeronave not found'}, 404
    except Exception as ex:
        print(ex)
        return {'error': 'An error occurred'}, 401


@planes_bp.delete('/<str:registration>')
def delete_plane_endp(registration: str):
    try:
        respuesta = disable_plane(registration)
        if respuesta:
            return {'message': 'Aeronave deleted successfully'}, 200
        else:
            return {'error': 'Aeronave not found'}, 404
    except Exception as ex:
        print(ex)
        return {'error': 'An error occurred'}, 401
