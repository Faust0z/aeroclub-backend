from app.models.users import Users
from ..services.balances import create_balance_srv
from sqlalchemy.orm import joinedload
from ..extensions import db

from datetime import datetime
from operator import or_
from app.models.roles import Roles


def obtenerUsuarioPorEmail(mail):
    # Cargar la relación 'roles' utilizando joinedload
    userMalFormato = db.session.query(Users).filter_by(email=mail).options(joinedload(Users.roles)).first()

    if not userMalFormato:
        return False

    usuario = {'id_usuarios': userMalFormato.id_usuarios,
               'nombre': userMalFormato.first_name,
               'apellido': userMalFormato.last_name,
               'email': userMalFormato.email,
               'telefono': userMalFormato.phone_number,
               'dni': userMalFormato.dni,
               'fecha_alta': userMalFormato.created_at,
               'fecha_baja': userMalFormato.disabled_at,
               'direccion': userMalFormato.address,
               'foto_perfil': userMalFormato.foto_perfil,
               'estado_hab_des': userMalFormato.status,
               'roles': [
                   {
                       'id_roles': role.id,
                       'tipo': role.name,
                   }
                   for role in userMalFormato.roles
               ]

               }
    return usuario

def obtenerUsuarios():
    # Cargar la relación 'roles' utilizando joinedload
    users = db.session.query(Users).options(joinedload(Users.roles)).all()

    users = Users.query.all()
    user_list = [{'id_usuarios': user.id_usuarios,
                  'nombre': user.first_name,
                  'apellido': user.last_name,
                  'email': user.email,
                  'telefono': user.phone_number,
                  'dni': user.dni,
                  'fecha_alta': user.created_at,
                  'fecha_baja': user.disabled_at,
                  'direccion': user.address,
                  'foto_perfil': user.foto_perfil,
                  'estado_hab_des': user.status,
                  'roles': [
                      {
                          'id_roles': role.id,
                          'tipo': role.name,
                      }
                      for role in user.roles
                  ]  # Incluye los datos de la relación 'roles'
                  } for user in users if user.status != 0]
    return user_list

def crearUsuario(data):
    try:
        id_usuarios = data.get('id_usuarios')
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        email = data.get('email')
        telefono = data.get('telefono')
        dni = data.get('dni')
        fecha_alta = data.get('fecha_alta')
        fecha_baja = data.get('fecha_baja')
        direccion = data.get('direccion')
        foto_perfil = data.get('foto_perfil')
        estado_hab_des = data.get('estado_hab_des')

        fecha_alta = datetime.now()
        estado_hab_des = 1
        # hacer un control exacto de cada input para devolver el error exacto
        if not email:
            return False

        usuario = Users(id_usuarios=id_usuarios, nombre=nombre, apellido=apellido,
                        email=email, telefono=telefono,
                        dni=dni, fecha_alta=fecha_alta,
                        fecha_baja=fecha_baja, direccion=direccion,
                        foto_perfil=foto_perfil, estado_hab_des=estado_hab_des)
        db.session.add(usuario)
        db.session.commit()

        # se crea la cuenta del usuario
        create_balance_srv(usuario.id_usuarios)
        return True
    except Exception as ex:
        print(ex.args)
        return False

def editarUsuario(email, data):
    # solo trae el dicc y no la clase de la bd
    user = obtenerUsuarioPorEmail(email)
    # te trae un usuario de la bd
    usuario = Users.query.get(user["id_usuarios"])

    if not usuario:
        return False

    if 'nombre' in data:
        usuario.first_name = data['nombre']
    if 'apellido' in data:
        usuario.last_name = data['apellido']
    if 'email' in data:
        usuario.email = data['email']
    if 'telefono' in data:
        usuario.phone_number = data['telefono']
    if 'dni' in data:
        usuario.dni = data['dni']
    if 'fecha_alta' in data:
        usuario.created_at = data['fecha_alta']
    if 'fecha_baja' in data:
        usuario.disabled_at = data['fecha_baja']
    if 'direccion' in data:
        usuario.address = data['direccion']
    if 'foto_perfil' in data:
        usuario.foto_perfil = data['foto_perfil']
    if 'estado_hab_des' in data:
        usuario.status = data['estado_hab_des']

    # para que te lo guarde primero hay que buscar en la db una clase del modelo
    # y despues cuando modifique un atributo de esa clase cuenta como que lo modifique
    # y ahi el commit me lo toma como un cambio y lo guarda
    db.session.commit()
    return True

def eliminarUsuario(email):
    user = obtenerUsuarioPorEmail(email)
    usuario = Users.query.get(user["id_usuarios"])

    if not usuario:
        return False

    usuario.status = 0
    db.session.commit()
    return True

def obtenerUsuarioPorNombre(nombre):
    usuarioNombre = db.session.query(Users).filter(
        or_(Users.first_name.like(f'%{nombre}%'), Users.last_name.like(f'%{nombre}%'))).all()
    if not usuarioNombre:
        return False

    resultados_json = [
        {'id_usuarios': usuario.id_usuarios, 'nombre': usuario.first_name, 'apellido': usuario.last_name,
         'email': usuario.email}
        for usuario in usuarioNombre]

    return resultados_json

def obtenerInstructores():
    try:
        # Obtener id_usuarios de UsersHaveRoles con id_roles == 2
        rolInstructor = db.session.query(Roles).filter_by(tipo='Instructor').first()
        instructores_id = db.session.query(Users).filter_by(roles_id=rolInstructor.id).all()

        # Almacena los id_usuarios en una lista
        id_usuarios_rol_dos = [usuario.user_id for usuario in instructores_id]

        # Obtener los datos de los usuarios del array id_usuarios_rol_dos
        instructores_list = db.session.query(Users).filter(Users.id_usuarios.in_(id_usuarios_rol_dos)).all()

        # Construir la lista con los datos de cada instrutor
        instructores_data = [
            {
                'id_usuarios': instructor.id_usuarios,
                'nombre': instructor.first_name,
                'apellido': instructor.last_name,
                'email': instructor.email,
                'telefono': instructor.phone_number,
                'dni': instructor.dni,
                'fecha_alta': instructor.created_at,
                'fecha_baja': instructor.disabled_at,
                'direccion': instructor.address,
                'foto_perfil': instructor.foto_perfil,
                'estado_hab_des': instructor.status,
                'roles': [
                    {
                        'id_roles': rol.id,
                        'tipo': rol.name,
                    }
                    for rol in instructor.roles if rol.id == 2
                ]
            }
            for instructor in instructores_list if instructor.status != 0
        ]

        return instructores_data
    except Exception as ex:
        print(ex.args)
        return False

def obtenerAsociados():
    try:
        # Obtener id_usuarios de UsersHaveRoles con id_roles == 2
        rolAsociado = db.session.query(Roles).filter_by(tipo='Asociado').first()
        asociado_id = db.session.query(Users).filter_by(roles_id=rolAsociado.id).all()

        # Almacena los id_usuarios en una lista
        id_usuarios_rol_asociado = [usuario.user_id for usuario in asociado_id]

        # Obtener los datos de los usuarios del array id_usuarios_rol_asociado
        asociados_list = db.session.query(Users).filter(Users.id_usuarios.in_(id_usuarios_rol_asociado)).all()

        # Construir la lista con los datos de cada instrutor
        asociados_data = [
            {
                'id_usuarios': asociado.id_usuarios,
                'nombre': asociado.first_name,
                'apellido': asociado.last_name,
                'email': asociado.email,
                'telefono': asociado.phone_number,
                'dni': asociado.dni,
                'fecha_alta': asociado.created_at,
                'fecha_baja': asociado.disabled_at,
                'direccion': asociado.address,
                'foto_perfil': asociado.foto_perfil,
                'estado_hab_des': asociado.status,
                'roles': [
                    {
                        'id_roles': rol.id,
                        'tipo': rol.name,
                    }
                    for rol in asociado.roles if rol.id
                ]
            }
            for asociado in asociados_list if asociado.status != 0
        ]

        return asociados_data
    except Exception as ex:
        print(ex.args)
        return False
