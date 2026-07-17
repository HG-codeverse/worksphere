from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    url_for
)

from flask_jwt_extended import jwt_required

from app.members.forms import MemberForm
from app.members.service import (
    create_member,
    get_members
)
from app.utils.auth import admin_required
from flask import request

member_bp = Blueprint(
    "members",
    __name__,
    url_prefix="/members"
)


@member_bp.route("/")
@jwt_required()
@admin_required
def list_members():

    search = request.args.get("search", "")

    members = get_members(search)

    return render_template(
        "members/list.html",
        members=members,
        search=search
    )

@member_bp.route("/create", methods=["GET", "POST"])
@jwt_required()
@admin_required
def create():

    form = MemberForm()

    if form.validate_on_submit():

        success, message = create_member(form)

        flash(message)

        if success:
            return redirect(
                url_for("members.list_members")
            )

    return render_template(
        "members/create.html",
        form=form
    )