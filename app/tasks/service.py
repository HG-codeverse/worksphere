from app.extensions import db
from app.models.project import Project
from app.models.task import Task
from app.models.user import User
from app.utils.auth import current_user
from app.activity.service import log_activity
from sqlalchemy import or_


def load_dropdowns(form):

    user = current_user()

    form.project.choices = [
        (p.id, p.name)
        for p in Project.query.filter_by(
            organization_id=user.organization_id
        ).all()
    ]

    form.assignee.choices = [
        (u.id, u.name)
        for u in User.query.filter_by(
            organization_id=user.organization_id
        ).all()
    ]


def create_task(form):
    user = current_user()

    task = Task(
        project_id=form.project.data,
        assigned_to=form.assignee.data,
        title=form.title.data,
        description=form.description.data,
        priority=form.priority.data,
        status=form.status.data,
        due_date=form.due_date.data
    )

    db.session.add(task)
    db.session.commit()
    log_activity(
        user,
        f"Created task '{task.title}'"
    )
     

    return True, "Task Created Successfully"


def get_tasks(search=""):

    user = current_user()

    query = (
        Task.query
        .join(Project)
        .filter(
            Project.organization_id == user.organization_id
        )
    )

    if search:

        query = query.filter(
            or_(
                Task.title.ilike(f"%{search}%"),
                Task.description.ilike(f"%{search}%"),
                Task.status.ilike(f"%{search}%")
            )
        )

    return (
        query
        .order_by(Task.created_at.desc())
        .all()
    )
def get_task(task_id):

    user = current_user()

    return (
        Task.query
        .join(Project)
        .filter(
            Task.id == task_id,
            Project.organization_id == user.organization_id
        )
        .first()
    )


def update_task(task, form):
    user = current_user()
    task.title = form.title.data
    task.description = form.description.data
    task.priority = form.priority.data
    task.status = form.status.data
    task.project_id = form.project.data
    task.assigned_to = form.assignee.data
    task.due_date = form.due_date.data

    db.session.commit()
    log_activity(
        user,
        f"Updated task '{task.title}'"
    )
    return True, "Task Updated Successfully"


def delete_task(task_id):
    user = current_user()
    task = get_task(task_id)
    task_name = task.title
    if not task:
        return False, "Task not found"

    db.session.delete(task)
    db.session.commit()
    log_activity(
        user,
        f"Deleted task '{task_name}'"
    )

    return True, "Task Deleted Successfully"