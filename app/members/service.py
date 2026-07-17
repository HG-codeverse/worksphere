from app.extensions import db
from app.models.user import User
from app.utils.auth import current_user
from app.utils.constants import UserRole
from app.activity.service import log_activity
from sqlalchemy import or_

def create_member(form):

    admin = current_user()

    if User.query.filter_by(email=form.email.data).first():
        return False, "Email already exists."

    member = User(
        organization_id=admin.organization_id,
        name=form.name.data,
        email=form.email.data,
        role=UserRole.MEMBER
    )

    member.set_password(form.password.data)

    db.session.add(member)
    db.session.commit()
    log_activity(
        admin,
        f"Added member '{member.name}'"
    )

    return True, "Member Created Successfully"


def get_members(search=""):

    admin = current_user()

    query = User.query.filter_by(
        organization_id=admin.organization_id
    )

    if search:

        query = query.filter(
            or_(
                User.name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
        )

    return query.order_by(
        User.created_at.desc()
    ).all()