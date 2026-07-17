from functools import wraps

from flask import flash, redirect, url_for
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt_identity
)

from app.models.user import User
from app.utils.constants import UserRole


def current_user():

    verify_jwt_in_request()

    return User.query.get(
        int(get_jwt_identity())
    )


def admin_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        user = current_user()

        if not user:
            flash("User not found.")
            return redirect(url_for("auth.login"))

        if user.role != UserRole.ADMIN:
            flash("Only administrators can perform this action.")
            return redirect(url_for("dashboard.dashboard"))

        return func(*args, **kwargs)

    return wrapper