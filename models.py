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
    score = db.Column(db.Integer, nullable=False)
    source = db.Column(db.String(50))

    feedback_date = db.Column(
        db.DateTime,
        nullable=False
    )
    # Datetime set by system
    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    # One-to-many as feedback may have analysis versions
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
    summary = db.Column(db.Text)
    analysis_json = db.Column(db.JSON)

    # Datetime set by system
    analyzed_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    #Captures version in case of re-analysis action
    analysis_version = db.Column(
        db.Integer,
        default=1,
        nullable=False
    )

    # Link to feedback table
    feedback_id = db.Column(
        db.Integer,
        db.ForeignKey("feedback.id"),
        nullable=False
    )
