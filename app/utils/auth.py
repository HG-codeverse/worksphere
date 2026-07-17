from flask_jwt_extended import get_jwt_identity

from app.models.user import User


def current_user():
    return User.query.get(int(get_jwt_identity()))