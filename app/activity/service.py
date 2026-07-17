from app.extensions import db
from app.models.activity_log import ActivityLog


def log_activity(user, action):

    activity = ActivityLog(
        organization_id=user.organization_id,
        user_id=user.id,
        action=action
    )

    db.session.add(activity)
    db.session.commit()


def recent_activity(user):

    return (
        ActivityLog.query
        .filter_by(
            organization_id=user.organization_id
        )
        .order_by(ActivityLog.created_at.desc())
        .limit(10)
        .all()
    )