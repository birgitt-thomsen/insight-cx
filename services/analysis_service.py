import time
from openai import RateLimitError
from flask import current_app
from collections import Counter
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

    def analyze_feedback_list(self, feedback):
        """
        Analyze a supplied list of Feedback objects.
        Used immediately after a CSV upload.
        """

        return self._process_feedback(feedback)

    def analyze_feedback(self, feedback):
        """
        Analyze a single feedback record.
        Used after a CSV upload or when re-analyzing
        an individual feedback item.
        """

        result = self.ai_service.analyze_feedback(
            feedback.comment
        )

        self.analysis_storage.save_or_update(
            feedback.id,
            result
        )

        return result

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

    def test_feedback(
            self,
            feedback,
            model=None,
            temperature=None,
            system_prompt_version=None,
            feedback_prompt_version=None,
    ):
        """
        Test a prompt against a single feedback item.
        Does not save anything.
        """

        return self._process_prompt_tests(
            feedback_items=[feedback],
            model=model,
            system_prompt_version=system_prompt_version,
            feedback_prompt_version=feedback_prompt_version,
        )

    def test_sample(
            self,
            model=None,
            temperature=None,
            system_prompt_version=None,
            feedback_prompt_version=None,
    ):
        """
        Test a prompt against the benchmark sample.
        Does not save anything.
        """

        feedback_items = (
            self.feedback_storage.get_test_sample()
        )

        return self._process_prompt_tests(
            feedback_items=feedback_items,
            model=model,
            temperature=temperature,
            system_prompt_version=system_prompt_version,
            feedback_prompt_version=feedback_prompt_version,
        )

    def _process_prompt_tests(
            self,
            feedback_items,
            model,
            temperature,
            system_prompt_version,
            feedback_prompt_version,
    ):
        """
        Execute prompt tests for a collection of feedback.
        Does not save anything.
        """

        results = []
        failures = []

        sentiment_counter = Counter()
        priority_counter = Counter()
        theme_counter = Counter()
        emotion_counter = Counter()
        confidence_total = 0
        confidence_count = 0

        for feedback in feedback_items:
            current_analysis = (
                self.analysis_storage.get_analysis(
                    feedback.id
                )
            )

            result = {
                "feedback": feedback,
                "current": current_analysis,
                "output": None,
                "error": None,
                "changed_fields": [],
            }

            max_retries = 4

            for attempt in range(max_retries):

                try:

                    output = self.ai_service.test_prompt(
                        feedback.comment,
                        model=model,
                        temperature=temperature,
                        system_prompt_version=system_prompt_version,
                        feedback_prompt_version=feedback_prompt_version,
                    )

                    result["output"] = output

                    result["changed_fields"] = (
                        self._compare_analysis(
                            result["current"],
                            output,
                        )
                    )

                    #
                    # Optional summary statistics
                    #

                    sentiment = output.get("sentiment")

                    if sentiment:
                        sentiment_counter[sentiment] += 1

                    emotion = output.get("emotion")

                    if emotion:
                        emotion_counter[emotion] += 1

                    confidence = output.get("confidence")

                    if confidence is not None:
                        confidence_total += float(confidence)
                        confidence_count += 1

                    priority = output.get("priority")

                    if priority:
                        priority_counter[priority] += 1

                    themes = output.get(
                        "themes",
                        []
                    )

                    for theme in themes:
                        theme_counter[theme] += 1

                    break

                except RateLimitError:

                    wait = 2 ** attempt

                    result["error"] = (
                        f"Rate limit. Retrying in {wait}s."
                    )

                    time.sleep(wait)

                except Exception as e:

                    result["error"] = str(e)

                    break

            if result["output"] is None:
                failures.append(
                    {
                        "feedback_id": feedback.id,
                        "error": result["error"],
                    }
                )

            results.append(result)

            #
            # Gentle throttling
            #

            time.sleep(1)

        #
        # Calculate summary statistics
        #

        average_confidence = 0

        if confidence_count:
            average_confidence = round(
                confidence_total / confidence_count,
                2
            )

        return {

            "total": len(feedback_items),

            "successful":
                len(results) - len(failures),

            "failed":
                len(failures),

            "results":
                results,

            "failures":
                failures,

            "statistics": {

                "sentiment":
                    dict(sentiment_counter),

                "emotion":
                    dict(emotion_counter),

                "priority":
                    dict(priority_counter),

                "average_confidence":
                    average_confidence,

                "themes":
                    # dict(theme_counter),
                    theme_counter.most_common(10)

            }

        }

    def _compare_analysis(
        self,
        current,
        output,
    ):
        """
        Compare an existing analysis with a new AI output.

        Returns:
            list[str]: Fields that changed.
        """

        if current is None:
            return []

        changed = []

        if current.sentiment != output.get("sentiment"):
            changed.append("sentiment")

        if current.emotion != output.get("emotion"):
            changed.append("emotion")

        if current.priority != output.get("priority"):
            changed.append("priority")

        if abs(
            current.confidence -
            output.get("confidence", 0)
        ) > 0.05:
            changed.append("confidence")

        if set(current.themes) != set(
            output.get("themes", [])
        ):
            changed.append("themes")

        if current.summary != output.get("summary"):
            changed.append("summary")

        return changed