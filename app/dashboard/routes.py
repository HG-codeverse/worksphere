from flask import Blueprint, render_template

from flask_jwt_extended import jwt_required

from app.models.project import Project
from app.models.task import Task
from app.utils.auth import current_user
from app.activity.service import recent_activity

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


@dashboard_bp.route("/")
@jwt_required()
def dashboard():

    user = current_user()
    activities = recent_activity(user)

    total_projects = Project.query.filter_by(
        organization_id=user.organization_id
    ).count()

    total_tasks = (
        Task.query.join(Project)
        .filter(Project.organization_id == user.organization_id)
        .count()
    )

    completed_tasks = (
        Task.query.join(Project)
        .filter(
            Project.organization_id == user.organization_id,
            Task.status == "Completed"
        )
        .count()
    )

    pending_tasks = (
        Task.query.join(Project)
        .filter(
            Project.organization_id == user.organization_id,
            Task.status != "Completed"
        )
        .count()
    )

    recent_projects = (
        Project.query.filter_by(
            organization_id=user.organization_id
        )
        .order_by(Project.created_at.desc())
        .limit(5)
        .all()
    )

    recent_tasks = (
        Task.query.join(Project)
        .filter(Project.organization_id == user.organization_id)
        .order_by(Task.created_at.desc())
        .limit(5)
        .all()
    )
    
    
    return render_template(
        "dashboard/dashboard.html",
        total_projects=total_projects,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        recent_projects=recent_projects,
        recent_tasks=recent_tasks,
        activities=activities
    )