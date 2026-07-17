from flask import request

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_jwt_extended import jwt_required

from app.tasks.forms import TaskForm
from app.tasks.service import (
    create_task,
    get_tasks,
    load_dropdowns,
    get_task,
    update_task,
    delete_task
)
from app.utils.auth import admin_required
task_bp = Blueprint(
    "tasks",
    __name__,
    url_prefix="/tasks"
)


@task_bp.route("/")
@jwt_required()
def list_tasks():

    search = request.args.get("search", "")

    tasks = get_tasks(search)

    return render_template(
        "tasks/list.html",
        tasks=tasks,
        search=search
    )

@task_bp.route("/create", methods=["GET", "POST"])
@jwt_required()
@admin_required
def create():

    form = TaskForm()

    load_dropdowns(form)

    if form.validate_on_submit():

        success, message = create_task(form)

        flash(message)

        if success:
            return redirect(
                url_for("tasks.list_tasks")
            )

    return render_template(
        "tasks/create.html",
        form=form
    )


@task_bp.route("/edit/<int:task_id>", methods=["GET", "POST"])
@jwt_required()
@admin_required
def edit(task_id):

    task = get_task(task_id)

    if not task:
        flash("Task not found")
        return redirect(url_for("tasks.list_tasks"))

    form = TaskForm(obj=task)

    load_dropdowns(form)

    if form.validate_on_submit():

        success, message = update_task(task, form)

        flash(message)

        if success:
            return redirect(url_for("tasks.list_tasks"))

    return render_template(
        "tasks/create.html",
        form=form
    )


@task_bp.route("/delete/<int:task_id>")
@jwt_required()
@admin_required
def delete(task_id):

    success, message = delete_task(task_id)

    flash(message)

    return redirect(url_for("tasks.list_tasks"))