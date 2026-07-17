from flask import Blueprint, flash, redirect, render_template, url_for

from app.auth.forms import RegistrationForm
from app.auth.service import register_organization

from app.auth.forms import LoginForm
from app.auth.service import login_user

from flask_jwt_extended import set_access_cookies
from flask import make_response


from flask_jwt_extended import unset_jwt_cookies
from flask import make_response
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        success, message = register_organization(form)

        flash(message)

        if success:
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        success, message, token = login_user(form)

        flash(message)

        if success:
            response = make_response(
                redirect(url_for("dashboard.dashboard"))
            )

            set_access_cookies(response, token)

            return response

    return render_template(
        "auth/login.html",
        form=form
    )


@auth_bp.route("/logout")
def logout():

    response = make_response(
        redirect(url_for("auth.login"))
    )

    unset_jwt_cookies(response)

    flash("Logged out successfully")

    return response