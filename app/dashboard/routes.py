from flask import Blueprint, render_template

from flask_jwt_extended import jwt_required

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


@dashboard_bp.route("/")
@jwt_required()
def dashboard():

    return render_template(
        "dashboard/dashboard.html"
    )