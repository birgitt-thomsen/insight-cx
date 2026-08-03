"""This script builds the data summary for the executive insight prompt."""

from collections import Counter
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from models import db, Feedback, Analysis
from storage.executive_insights_storage import ExecutiveInsightsStorage


class ExecutiveDataService:
    """
    Builds an aggregated dataset that can be consumed
    by AI insight services.
    """
    def __init__(self):
        self.executive_storage = ExecutiveInsightsStorage()


    def build_summary_data(self):
        """
        Return an aggregated business dataset.
        """

        analyses = (
            Analysis.query
            .options(
                joinedload(Analysis.feedback)
            )
            .all()
        )

        latest_summary = (
            self.executive_storage
            .get_latest_summary()
        )

        previous_summary = (
            self.executive_storage
            .get_previous_summary()
        )

        comparison_context = None

        if previous_summary:
            comparison_context = {

                "customer_health":
                    previous_summary.summary_json.get(
                        "customer_health"
                    ),

                "top_business_drivers":
                    previous_summary.summary_json.get(
                        "top_business_drivers",
                        []
                    )
            }

        return {

            "metrics": self._get_metrics(),

            "business_drivers": self._get_top_reason_codes(
                analyses
            ),

            "sentiment": self._get_sentiment(
                analyses
            ),

            "priority": self._get_priority(
                analyses
            ),

            "emotions": self._get_emotions(
                analyses
            ),

            "comments": self._get_representative_comments(
                analyses
            ),

            "previous_period":
                comparison_context,

            # "comparison": {
            #
            #     "latest": (
            #         latest_summary.summary_json
            #         if latest_summary
            #         else None
            #     ),
            #
            #     "previous": (
            #         previous_summary.summary_json
            #         if previous_summary
            #         else None
            #     )
            # }

        }

    def _get_metrics(self):
        """
        Return overall business metrics.
        """

        total_feedback = Feedback.query.count()

        #
        # NPS
        #

        total_nps = Feedback.query.filter_by(
            survey_type="NPS"
        ).count()

        nps_counts = dict(

            db.session.query(
                Feedback.nps_category,
                func.count()
            )
            .group_by(
                Feedback.nps_category
            )
            .all()

        )

        #
        # CSAT
        #

        total_csat = Feedback.query.filter_by(
            survey_type="CSAT"
        ).count()

        csat_counts = dict(

            db.session.query(
                Feedback.csat_category,
                func.count()
            )
            .group_by(
                Feedback.csat_category
            )
            .all()

        )

        return {

            "feedback_count": total_feedback,

            "nps": {

                "total": total_nps,

                "promoters": nps_counts.get(
                    "Promoter",
                    0
                ),

                "passives": nps_counts.get(
                    "Passive",
                    0
                ),

                "detractors": nps_counts.get(
                    "Detractor",
                    0
                ),
            },

            "csat": {

                "total": total_csat,

                "satisfied": csat_counts.get(
                    "Satisfied",
                    0
                ),

                "neutral": csat_counts.get(
                    "Neutral",
                    0
                ),

                "dissatisfied": csat_counts.get(
                    "Dissatisfied",
                    0
                ),
            }
        }

    def _get_top_reason_codes(
            self,
            analyses
    ):
        """
        Return the most common primary reason codes.
        """

        counter = Counter()

        for analysis in analyses:

            if not analysis.reason_codes:
                continue

            for reason in analysis.reason_codes:

                if reason.get("rank") == 1:
                    counter[reason["code"]] += 1

        return [

            {
                "theme": code,
                "count": count,
            }

            for code, count
            in counter.most_common(5)

        ]

    def _get_sentiment(
        self,
        analyses
    ):
        """
        Return sentiment distribution.
        """

        counter = Counter()

        for analysis in analyses:

            if analysis.sentiment:

                counter[
                    analysis.sentiment
                ] += 1

        total = sum(
            counter.values()
        )

        return [

            {
                "sentiment": sentiment,

                "count": count,

                "percentage": round(
                    (count / total) * 100,
                    1
                ) if total else 0

            }

            for sentiment, count
            in counter.items()

        ]

    def _get_priority(
        self,
        analyses
    ):
        """
        Return priority distribution.
        """

        counter = Counter()

        for analysis in analyses:

            if analysis.priority:

                counter[
                    analysis.priority
                ] += 1

        return [

            {
                "priority": priority,
                "count": count
            }

            for priority, count
            in counter.items()

        ]

    def _get_emotions(
            self,
            analyses
    ):
        """
        Return emotion distribution.
        """

        counter = Counter()

        for analysis in analyses:

            if not analysis.emotions:
                continue

            for emotion in analysis.emotions:
                counter[emotion] += 1

        return [

            {
                "emotion": emotion,
                "count": count
            }

            for emotion, count
            in counter.most_common()

        ]

    def _get_representative_comments(
            self,
            analyses,
    ):
        """
        Return representative comments grouped by primary reason code.
        """

        comments = {}

        for analysis in analyses:

            if (
                    not analysis.feedback
                    or not analysis.reason_codes
            ):
                continue

            primary_reason = next(

                (
                    reason["code"]
                    for reason in analysis.reason_codes
                    if reason.get("rank") == 1
                ),

                None

            )

            if not primary_reason:
                continue

            comments.setdefault(
                primary_reason,
                []
            )

            if len(comments[primary_reason]) < 3:
                comments[primary_reason].append({

                    "sentiment": analysis.sentiment,

                    "emotions": analysis.emotions,

                    "intent": analysis.intent,

                    "priority": analysis.priority,

                    "business_signal": analysis.business_signal,

                    "comment": analysis.feedback.comment

                })

        return comments