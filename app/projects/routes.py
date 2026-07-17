from flask import Blueprint, flash, redirect, render_template, url_for

from flask_jwt_extended import jwt_required

from app.projects.forms import ProjectForm

from app.utils.auth import admin_required
from flask import request

from app.projects.service import (
    create_project,
    get_projects,
    get_project,
    update_project,
    delete_project
)


project_bp = Blueprint(
    "projects",
    __name__,
    url_prefix="/projects"
)


@project_bp.route("/")
@jwt_required()
def list_projects():

    search = request.args.get("search", "")

    projects = get_projects(search)

    return render_template(
        "projects/list.html",
        projects=projects,
        search=search
    )

@project_bp.route("/create", methods=["GET", "POST"])
@jwt_required()
@admin_required
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

@project_bp.route("/edit/<int:project_id>", methods=["GET", "POST"])
@jwt_required()
@admin_required
def edit(project_id):

    project = get_project(project_id)

    if not project:
        flash("Project not found")
        return redirect(url_for("projects.list_projects"))

    form = ProjectForm(obj=project)

    if form.validate_on_submit():

        success, message = update_project(
            project,
            form
        )

        flash(message)

        if success:
            return redirect(url_for("projects.list_projects"))

    return render_template(
        "projects/create.html",
        form=form
    )


@project_bp.route("/delete/<int:project_id>")
@jwt_required()
@admin_required
def delete(project_id):

    success, message = delete_project(project_id)

    flash(message)

    return redirect(url_for("projects.list_projects"))

