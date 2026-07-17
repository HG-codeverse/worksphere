from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models.project import Project
from app.models.user import User


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

    return True, "Project Created Successfully"


def get_projects():

    user = current_user()

    return Project.query.filter_by(
        organization_id=user.organization_id
    ).order_by(
        Project.created_at.desc()
    ).all()