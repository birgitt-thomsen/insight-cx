""" Defines data tables for the application. """
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Feedback(db.Model):
    """ Defines columns for feedback table. """

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_id = db.Column(db.String(20), nullable=False)
    order_number = db.Column(db.String(25), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    survey_type = db.Column(db.String(20), nullable=False)
    survey_score = db.Column(db.Integer)
    source = db.Column(db.String(50))

    # Datetime set by system
    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Link to Analysis
    analyses = db.relationship(
        "Analysis",
        backref="feedback",
        lazy=True
    )


class Analysis(db.Model):
    """ Defines columns for analysis table. """

    id = db.Column(db.Integer, primary_key=True)
    sentiment = db.Column(db.String(20), nullable=False)
    emotion = db.Column(db.String(30))
    themes = db.Column(db.JSON)
    priority = db.Column(db.String(20))
    confidence = db.Column(db.Float)
    insight = db.Column(db.Text)
    analysis_json = db.Column(db.JSON)
    analyzed_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    # Link to feedback table
    feedback_id = db.Column(
        db.Integer,
        db.ForeignKey("feedback.id"),
        nullable=False
    )
