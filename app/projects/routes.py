from flask import Blueprint, flash, redirect, render_template, url_for

from flask_jwt_extended import jwt_required

from app.projects.forms import ProjectForm
from app.projects.service import create_project, get_projects

project_bp = Blueprint(
    "projects",
    __name__,
    url_prefix="/projects"
)


@project_bp.route("/")
@jwt_required()
def list_projects():

    projects = get_projects()

    return render_template(
        "projects/list.html",
        projects=projects
    )


@project_bp.route("/create", methods=["GET", "POST"])
@jwt_required()
def create():

    form = ProjectForm()

    if form.validate_on_submit():

        success, message = create_project(form)

        flash(message)

        if success:

            return redirect(
                url_for("projects.list_projects")
            )

    return render_template(
        "projects/create.html",
        form=form
    )