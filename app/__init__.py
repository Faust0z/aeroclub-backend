from flask import Flask
import os
from flask_migrate import Migrate
from flask_cors import CORS
from app.controllers.users import users_bp
from app.controllers.planes import planes_bp
from app.controllers.roles import roles_bp
from app.controllers.invoices import invoices_bp
from app.controllers.auth import auth_bp
from app.controllers.transactions import transactions_bp
from app.controllers.balances import balances_bp
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

    app.register_blueprint(users_bp, url_prefix='/usuarios')
    app.register_blueprint(planes_bp, url_prefix='/aeronaves')
    app.register_blueprint(roles_bp, url_prefix='/roles')
    app.register_blueprint(invoices_bp, url_prefix='/recibo-vuelos')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(transactions_bp, url_prefix='/transacciones')
    app.register_blueprint(balances_bp, url_prefix='/cuentaCorriente')
    app.register_blueprint(PDF_invoices_bp, url_prefix='/recibo-pdf')

    return app
