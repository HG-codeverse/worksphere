from flask import Flask, flash, redirect, url_for, render_template

from app.config import Config
from app.extensions import db, migrate, jwt


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.models import Organization, User, Project, Task, ActivityLog

    from app.auth.routes import auth_bp
    from app.dashboard.routes import dashboard_bp
    from app.projects.routes import project_bp
    from app.tasks.routes import task_bp
    from app.members.routes import member_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(member_bp)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template(
            "errors/404.html"
        ), 404

    @app.errorhandler(403)
    def forbidden(error):
        return render_template(
            "errors/403.html"
        ), 403

    @app.errorhandler(500)
    def internal_server_error(error):
        db.session.rollback()
        return render_template(
            "errors/500.html"
        ), 500

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        flash("Please login first.")
        return redirect(url_for("auth.login"))

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        flash("Invalid session. Please login again.")
        return redirect(url_for("auth.login"))

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        flash("Session expired. Please login again.")
        return redirect(url_for("auth.login"))

    with app.app_context():
        db.create_all()

    return app