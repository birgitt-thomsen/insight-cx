""" This script handles the interaction with the feedback table. """
from sqlalchemy import insert
from models import db, Feedback

class FeedbackStorage:

    def add_feedback(self, records):
        """Insert feedback records into the database."""

        try:
            feedback_objects = [
                Feedback(**record)
                for record in records
            ]

            db.session.add_all(feedback_objects)
            db.session.commit()

            return len(feedback_objects)

        except Exception:
            db.session.rollback()
            raise
