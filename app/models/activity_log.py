from datetime import datetime,UTC
from zoneinfo import ZoneInfo

from app.extensions import db


class ActivityLog(db.Model):
    __tablename__ = "activity_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    organization_id = db.Column(
        db.Integer,
        db.ForeignKey("organizations.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    action = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
    db.DateTime,
    default=lambda: datetime.now(UTC)
)


    user = db.relationship(
        "User",
        backref="activity_logs"
    )

    organization = db.relationship(
        "Organization",
        backref="activity_logs"
    )

    def __repr__(self):
        return f"<Activity {self.action}>"