from flask import current_app
from services.ai_service import AIService
from storage.analysis_storage import AnalysisStorage
from storage.feedback_storage import FeedbackStorage


class AnalysisService:
    """Coordinates AI analysis and persistence."""

    def __init__(self):
        self.ai_service = AIService()
        self.analysis_storage = AnalysisStorage()
        self.feedback_storage = FeedbackStorage()

    def _process_feedback(self, feedback_records):
        """Analyze a collection of feedback records."""

        processed = 0
        failed = 0

        for feedback in feedback_records:

            try:

                self.analyze_feedback(feedback)
                processed += 1


            except Exception:

                current_app.logger.exception(
                    f"Failed to analyze feedback "
                    f"{feedback.id}"
                )

                failed += 1

        return {
            "processed": processed,
            "failed": failed,
        }

    def analyze_feedback(self, feedback):
        """
        Analyze a single feedback record.

        Used after a CSV upload or when re-analyzing
        an individual feedback item.
        """

        analysis = self.ai_service.analyze_feedback(
            feedback.comment
        )

        self.analysis_storage.save_or_update(
            feedback.id,
            analysis
        )

        return analysis

    def initial_analysis(self):
        """
        Analyze every feedback record.
        Typically only used the very first time.
        """

        feedback_records = (
            self.feedback_storage.get_all_feedback()
        )

        return self._process_feedback(feedback_records)

    def analyze_pending_feedback(self):
        """
        Analyze feedback that has not yet been analyzed.
        Called automatically after each CSV upload.
        """

        feedback_records = (
            self.feedback_storage.get_unanalyzed_feedback()
        )

        return self._process_feedback(feedback_records)

    def reanalyze(self, feedback_id):
        """
        Re-analyze a single feedback record.
        """

        feedback = self.feedback_storage.get_feedback(
            feedback_id
        )

        if feedback is None:
            raise ValueError("Feedback not found.")

        self.analyze_feedback(feedback)

        return feedback

    def reanalyze_all(self):
        """
        Re-analyze every feedback record using
        the current prompt and model.
        """

        feedback_records = (
            self.feedback_storage.get_all_feedback()
        )

        return self._process_feedback(feedback_records)

    def _process_feedback(self, feedback_records):
        processed = 0
        failed = 0

        for feedback in feedback_records:
            try:
                self.analyze_feedback(feedback)
                processed += 1
            except Exception:
                failed += 1

        return {
            "processed": processed,
            "failed": failed
        }