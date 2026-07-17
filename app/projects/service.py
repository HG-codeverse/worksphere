from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models.project import Project
from app.models.user import User
from app.utils.auth import current_user
from app.activity.service import log_activity


def current_user():

    return User.query.get(
        int(get_jwt_identity())
    )


def create_project(form):

    user = current_user()

    project = Project(
        organization_id=user.organization_id,
        created_by=user.id,
        name=form.name.data,
        description=form.description.data,
        status=form.status.data
    )

    db.session.add(project)

    db.session.commit()
    log_activity(
    user,
        f"Created project '{project.name}'"
    )

    return True, "Project Created Successfully"


from sqlalchemy import or_

def get_projects(search=""):

    user = current_user()

    query = Project.query.filter_by(
        organization_id=user.organization_id
    )

    if search:

        query = query.filter(
            or_(
                Project.name.ilike(f"%{search}%"),
                Project.description.ilike(f"%{search}%"),
                Project.status.ilike(f"%{search}%")
            )
        )

    return query.order_by(
        Project.created_at.desc()
    ).all()

def get_project(project_id):

    user = current_user()

    return Project.query.filter_by(
        id=project_id,
        organization_id=user.organization_id
    ).first()


def update_project(project, form):
    user = current_user()
    project.name = form.name.data
    project.description = form.description.data
    project.status = form.status.data

    db.session.commit()
    log_activity(
        user,
        f"Updated project '{project.name}'"
    )

    return True, "Project Updated Successfully"


def delete_project(project_id):

    project = get_project(project_id)

    if not project:
        return False, "Project not found"
    
    project_name = project.name
    user = current_user()

    db.session.delete(project)

    db.session.commit()
    log_activity(
    user,
        f"Deleted project '{project_name}'"
    )

    return True, "Project Deleted Successfully"