from sqlalchemy.exc import IntegrityError
from slugify import slugify

from app.extensions import db
from app.models.organization import Organization
from app.models.user import User
from app.utils.constants import UserRole


def register_organization(form):
    try:
        if Organization.query.filter_by(email=form.company_email.data).first():
            return False, "Organization email already exists"

        if User.query.filter_by(email=form.admin_email.data).first():
            return False, "Admin email already exists"

        organization = Organization(
            name=form.company_name.data,
            email=form.company_email.data,
            slug=slugify(form.company_name.data)
        )

        db.session.add(organization)
        db.session.flush()

        admin = User(
            organization_id=organization.id,
            name=form.admin_name.data,
            email=form.admin_email.data,
            role=UserRole.ADMIN
        )

        admin.set_password(form.password.data)

        db.session.add(admin)

        db.session.commit()

        return True, "Registration Successful"

    except IntegrityError:
        db.session.rollback()
        return False, "Database Error"

    except Exception as e:
        db.session.rollback()
        print(e)
        return False, str(e)
    
from flask_jwt_extended import create_access_token


def login_user(form):

    user = User.query.filter_by(email=form.email.data).first()

    if not user:
        return False, "Invalid Credentials", None

    if not user.check_password(form.password.data):
        return False, "Invalid Credentials", None

    token = create_access_token(identity=str(user.id))

    return True, "Login Successful", token