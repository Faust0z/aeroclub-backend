from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from app.controllers.airport_codes import airport_codes_bp
from app.controllers.balances import balances_bp
from app.controllers.flight_sessions import flight_sessions_bp
from app.controllers.payment_types import payment_types_bp
from app.controllers.plane_status import plane_status_bp
from app.controllers.planes import planes_bp
from app.controllers.roles import roles_bp
from app.controllers.transactions import transactions_bp
from app.controllers.users import users_bp
from .config.settings import DB_URI, SQLA_TRACK_MODIFICATIONS, SECRET_KEY, DEBUG, CORS_ORIGINS
from .extensions import db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLA_TRACK_MODIFICATIONS
    app.config["JWT_SECRET_KEY"] = SECRET_KEY
    app.config["DEBUG"] = DEBUG

    jwt = JWTManager(app)

    db.init_app(app)

    CORS(app, resources={r"/*": {"origins": CORS_ORIGINS}})

    with app.app_context():
        db.create_all()

    migrate = Migrate(app, db)

    app.register_blueprint(airport_codes_bp)
    app.register_blueprint(balances_bp)
    app.register_blueprint(payment_types_bp)
    app.register_blueprint(plane_status_bp)
    app.register_blueprint(planes_bp)
    app.register_blueprint(roles_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(planes_bp)
    app.register_blueprint(roles_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(balances_bp)

    return app
