from flask import Flask
import os
from flask_migrate import Migrate
from flask_cors import CORS
from app.routes.usuarios import usuarios_bp
from app.routes.aeronaves import aeronaves_bp
from app.routes.roles import roles_bp
from app.routes.reciboVuelos import reciboVuelos_bp
from app.routes.auth import auth_bp
from app.routes.reciboCombustible import reciboCombustible_bp
from app.routes.transacciones import transacciones_bp
from app.routes.cuentaCorriente import cuentaCorriente_bp
from app.routes.recibosPDF import reciboPDF_bp
from .extensions import db
from .config.settings import DB_URI, SQLA_TRACK_MODIFICATIONS, SECRET_KEY, DEBUG


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLA_TRACK_MODIFICATIONS
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["DEBUG"] = DEBUG

    db.init_app(app)

    CORS(app)

    with app.app_context():
        db.create_all()

    migrate = Migrate(app, db)

    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(aeronaves_bp, url_prefix='/aeronaves')
    app.register_blueprint(roles_bp, url_prefix='/roles')
    app.register_blueprint(reciboVuelos_bp, url_prefix='/recibo-vuelos')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(reciboCombustible_bp, url_prefix='/recibo-combustible')
    app.register_blueprint(transacciones_bp, url_prefix='/transacciones')
    app.register_blueprint(cuentaCorriente_bp, url_prefix='/cuentaCorriente')
    app.register_blueprint(reciboPDF_bp, url_prefix='/recibo-pdf')

    return app
