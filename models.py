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

    nps_category = db.Column(
        db.String(10)
    )

    csat_category = db.Column(
        db.String(10)
    )

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

    # Flog for benchmark sampling
    is_test_sample = db.Column(
        db.Boolean,
        nullable=False,
        default=False
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

    # AI model name
    model = db.Column(
        db.String(50),
        nullable=False
    )

    # Prompt version for re-analysis action
    system_prompt_version = db.Column(
        db.String(10),
        nullable=False,
        default="v1"
    )

    prompt_version = db.Column(
        db.String(10),
        nullable=False,
        default="v1"
    )

    #Captures version for re-analysis action
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

class AISettings(db.Model):
    """
    Stores the active AI configuration used by
    the production analysis pipeline.

    There should only ever be one row.
    """

    __tablename__ = "ai_settings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Active feedback model
    feedback_model = db.Column(
        db.String(50),
        nullable=False,
        default="gpt-5-mini"
    )

    # Active system prompt
    system_prompt_version = db.Column(
        db.String(10),
        nullable=False,
        default="v1"
    )

    feedback_prompt_version = db.Column(
        db.String(10),
        nullable=False,
        default="v1"
    )

    # Useful for models prior to GTP-5
    feedback_temperature = db.Column(
        db.Float,
        nullable=False,
        default=0.2
    )

    # Active executive model
    executive_model = db.Column(
        db.String(50),
        nullable=False,
        default="gpt-5-mini"
    )

    executive_prompt_version = db.Column(
        db.String(10),
        nullable=False,
        default="v1"
    )

    # Active executive temperature (gtp-4 only)
    executive_temperature = db.Column(
        db.Float,
        nullable=False,
        default=0.2
    )

    # Optional metadata
    description = db.Column(
        db.String(200)
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )



class ExecutiveInsight(db.Model):
    """ Stores execution insights to be displayed in the UI. """

    __tablename__ = "executive_insights"

    id = db.Column(db.Integer, primary_key=True)

    period_type = db.Column(db.String(20), nullable=False)
    # all_time
    # month
    # week
    # custom

    period_start = db.Column(db.Date, nullable=False)
    period_end = db.Column(db.Date, nullable=False)

    feedback_count = db.Column(db.Integer)

    summary_json = db.Column(db.JSON)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    model = db.Column(db.String(50))
    prompt_version = db.Column(db.String(10))


# class AISettings(db.Model):
#     """
#     Stores the active AI configuration used by
#     the production analysis pipeline.
#
#     There should only ever be one row.
#     """
#
#     __tablename__ = "ai_settings"
#
#     id = db.Column(
#         db.Integer,
#         primary_key=True
#     )
#
#     # Active OpenAI model
#     model = db.Column(
#         db.String(50),
#         nullable=False,
#         default="gpt-5-mini"
#     )
#
#     # Active prompt versions
#     system_prompt_version = db.Column(
#         db.Integer,
#         nullable=False,
#         default=1
#     )
#
#     feedback_prompt_version = db.Column(
#         db.Integer,
#         nullable=False,
#         default=1
#     )
#
#     # Useful for models prior to GTP-5
#     temperature = db.Column(
#         db.Float,
#         nullable=False,
#         default=0.2
#     )
#
#     # Optional metadata
#     description = db.Column(
#         db.String(200)
#     )
#
#     updated_at = db.Column(
#         db.DateTime,
#         default=datetime.utcnow,
#         onupdate=datetime.utcnow,
#         nullable=False
#     )