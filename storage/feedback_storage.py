""" This script handles the interaction with the feedback table. """
from models import db, Feedback, Analysis
from sqlalchemy import select

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

            # IDs are populated after commit
            return feedback_objects

        except Exception:
            db.session.rollback()
            raise

    def get_feedback_page(
            self,
            page=1,
            per_page=25,
            filters=None
    ):
        """
        Return a paginated list of feedback records.

        Args:
            page (int): Page number.
            per_page (int): Records per page.
            filters (dict): Optional search, filter and sorting options.

        Returns:
            Pagination: Flask-SQLAlchemy Pagination object.
        """

        filters = filters or {}

        search = filters.get("search")
        survey_type = filters.get("survey_type")
        sentiment = filters.get("sentiment")
        priority = filters.get("priority")

        # ------------------------------------------------------
        # Base Query
        # ------------------------------------------------------

        query = (
            Feedback.query
            .join(Analysis)
        )

        # ------------------------------------------------------
        # Text Search
        # ------------------------------------------------------

        if search:
            query = query.filter(

                db.or_(

                    Feedback.customer_name.ilike(f"%{search}%"),

                    Feedback.order_number.ilike(f"%{search}%"),

                    Feedback.comment.ilike(f"%{search}%")

                )

            )

        # ------------------------------------------------------
        # Survey Type
        # ------------------------------------------------------

        if survey_type:
            query = query.filter(
                Feedback.survey_type == survey_type
            )

        # ------------------------------------------------------
        # Sentiment
        # ------------------------------------------------------

        if sentiment:
            query = query.filter(
                db.func.lower(Analysis.sentiment) == sentiment.lower()
            )

        # ------------------------------------------------------
        # Priority
        # ------------------------------------------------------

        if priority:
            query = query.filter(
                db.func.lower(Analysis.priority) == priority.lower()
            )

        # ------------------------------------------------------
        # Pagination
        # ------------------------------------------------------

        return query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
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

    def get_all_feedback(self):
        """Return all feedback records."""

        feedback = (
            select(Feedback)
            .order_by(Feedback.feedback_date.desc())
        )

        return db.session.scalars(feedback).all()


    def update_test_sample(
            self,
            feedback_id,
            selected
    ):
        """
        Add or remove a feedback item from
        the benchmark sample.
        """

        feedback = self.get_feedback(
            feedback_id
        )

        if feedback is None:
            return

        feedback.is_test_sample = selected

        db.session.commit()

        db.session.refresh(feedback)


    def get_test_sample(self):
        """
        Return all feedback included in the
        benchmark prompt test sample.
        """

        return (
            Feedback.query
            .filter_by(is_test_sample=True)
            .order_by(Feedback.feedback_date.desc())
            .all()
        )