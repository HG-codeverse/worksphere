from flask import Blueprint, flash, redirect, render_template, url_for

from app.auth.forms import RegistrationForm
from app.auth.service import register_organization

from app.auth.forms import LoginForm
from app.auth.service import login_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
    return redirect(url_for("auth.register"))


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
            return render_template(
                "dashboard/dashboard.html",
                token=token
            )

    return render_template(
        "auth/login.html",
        form=form
    )