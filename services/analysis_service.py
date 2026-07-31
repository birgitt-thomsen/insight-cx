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
            temperature=temperature,
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
        emotion_counter = Counter()
        intent_counter = Counter()
        confidence_counter = Counter()

        reason_code_counter = Counter()
        rank_1_reason_counter = Counter()
        rank_2_reason_counter = Counter()
        rank_3_reason_counter = Counter()

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

                    output = self.ai_service.execute_test_prompt(
                        feedback.comment,
                        model=model,
                        temperature=temperature,
                        system_prompt_version=system_prompt_version,
                        feedback_prompt_version=feedback_prompt_version,
                    )

                    # FOR TESTING ONLY
                    # print("\n====================")
                    # print(type(output))
                    # print(output)
                    # print("====================\n")

                    result["output"] = output

                    try:
                        result["changed_fields"] = (
                            self._compare_analysis(
                                result["current"],
                                output,
                            )
                        )
                    except Exception as e:
                        import traceback
                        traceback.print_exc()
                        raise

                    #
                    # Optional summary statistics
                    #

                    sentiment = output.get("sentiment")

                    # FOR TESTING ONLY
                    # print("Processing feedback:", feedback.id)
                    # print("Sentiment:", sentiment)

                    if sentiment:
                        sentiment_counter[sentiment] += 1

                    # FOR TESTING ONLY
                    # print(sentiment_counter)

                    for emotion in output.get("emotions", []):
                        emotion_counter[emotion] += 1

                    for intent in output.get("intent", []):
                        intent_counter[intent] += 1

                    priority = output.get("priority")

                    if priority:
                        priority_counter[priority] += 1

                    confidence = output.get("confidence")

                    if confidence:

                        # Average confidence score
                        score = confidence.get("score")

                        if score is not None:
                            confidence_total += float(score)
                            confidence_count += 1

                        # Distribution of confidence levels
                        level = confidence.get("level")

                        if level:
                            confidence_counter[level] += 1

                    #
                    # Reason code statistics
                    #

                    reason_codes = output.get(
                        "reason_codes",
                        []
                    )

                    for reason in reason_codes:

                        code = reason.get("code")

                        if not code:
                            continue

                        rank = reason.get("rank")

                        # Count every occurrence
                        reason_code_counter[code] += 1

                        # Count by rank
                        if rank == 1:
                            rank_1_reason_counter[code] += 1

                        elif rank == 2:
                            rank_2_reason_counter[code] += 1

                        elif rank == 3:
                            rank_3_reason_counter[code] += 1

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

                "emotions":
                    dict(emotion_counter),

                "intent":
                    dict(intent_counter),

                "priority":
                    dict(priority_counter),

                "confidence": {

                    "average_score": average_confidence,

                    "levels": dict(confidence_counter),

                },

                "reason_codes":
                    reason_code_counter.most_common(10),

                "primary_reason_codes":
                    rank_1_reason_counter.most_common(10),

                "secondary_reason_codes":
                    rank_2_reason_counter.most_common(10),

                "tertiary_reason_codes":
                    rank_3_reason_counter.most_common(10),

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

        #
        # Simple fields
        #

        if current.sentiment != output.get("sentiment"):
            changed.append("sentiment")

        if current.emotions != output.get("emotions", []):
            changed.append("emotions")

        if current.intent != output.get("intent", []):
            changed.append("intent")

        if current.priority != output.get("priority"):
            changed.append("priority")

        current_score = current.confidence_score or 0

        output_confidence = output.get("confidence", {})

        output_score = output_confidence.get("score", 0)
        output_level = output_confidence.get("level")

        if abs(current_score - output_score) >= 5:
            changed.append("confidence")

        elif current.confidence_level != output_level:
            changed.append("confidence")

        #
        # Reason codes
        #

        current_reason_codes = sorted(
            current.reason_codes or [],
            key=lambda r: r.get("rank", 99)
        )

        output_reason_codes = sorted(
            output.get("reason_codes", []),
            key=lambda r: r.get("rank", 99)
        )

        if current_reason_codes != output_reason_codes:
            changed.append("reason_codes")

        #
        # Business signal
        #

        if current.business_signal != output.get("business_signal"):
            changed.append("business_signal")

        return changed
