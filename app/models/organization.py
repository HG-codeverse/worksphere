from datetime import datetime, UTC

from app.extensions import db


class Organization(db.Model):
    __tablename__ = "organizations"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    slug = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )

    users = db.relationship(
        "User",
        backref="organization",
        lazy=True,
        cascade="all, delete-orphan"
    )

    projects = db.relationship(
        "Project",
        backref="organization",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Organization {self.name}>"