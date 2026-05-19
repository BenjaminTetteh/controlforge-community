from flask import Flask

from controlforge_web.config import Config

from controlforge_web.dashboard import dashboard_bp

from controlforge_web.findings import findings_bp

from flask_wtf.csrf import CSRFProtect

from flask_login import LoginManager

from controlforge_web.auth.user import (
    get_user_by_id
)

from controlforge_web.auth import auth_bp


csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    app.config.from_object(
        Config
    )

    csrf.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(
        auth_bp
    )
    
    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(user_id)
    

    @app.route("/")
    def index():
        return "ControlForge Web Dashboard is running."
    
    app.register_blueprint(
        dashboard_bp
    )    

    app.register_blueprint(
        findings_bp
    )

    

    return app

