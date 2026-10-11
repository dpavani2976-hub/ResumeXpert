from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(120),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    def __repr__(self):
        return f"<User {self.email}>"


# =======================================
# Resume Analysis Report
# =======================================

class Report(db.Model):

    __tablename__ = "reports"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    resume_name = db.Column(
        db.String(255),
        nullable=False
    )

    job_description_name = db.Column(
        db.String(255),
        nullable=True
    )

    ats_score = db.Column(
        db.Integer,
        nullable=False
    )

    matched_skills = db.Column(
        db.Integer,
        default=0
    )

    missing_skills = db.Column(
        db.Integer,
        default=0
    )

    analysis_date = db.Column(
        db.DateTime,
        nullable=False
    )