""" This script handles the interaction with the feedback table. """
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

    def get_feedback_page(self, page=1, per_page=25):
        """
        Return a paginated list of feedback records.

        Args:
            page (int): Page number (starting at 1).
            per_page (int): Number of records per page.

        Returns:
            Pagination: Flask-SQLAlchemy Pagination object.
        """

        return (
            Feedback.query
            .order_by(Feedback.feedback_date.desc())
            .paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
        )

    def get_feedback(self, feedback_id):
        """Return a single feedback item."""

        return db.session.get(
            Feedback,
            feedback_id
        )

    def remove_feedback(self, feedback_id):
        """Delete a feedback item."""

        feedback = db.session.get(
            Feedback,
            feedback_id
        )

        if feedback is None:
            return False

        db.session.delete(feedback)
        db.session.commit()

        return True

    def delete_all(self):
        """Delete every feedback record."""

        try:

            Feedback.query.delete()
            db.session.commit()

        except Exception:

            db.session.rollback()

            raise
