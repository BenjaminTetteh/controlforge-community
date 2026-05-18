from flask import Flask

from controlforge_web.config import Config

from controlforge_web.dashboard import dashboard_bp

from controlforge_web.findings import findings_bp



def create_app():

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    app.config.from_object(
        Config
    )

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

