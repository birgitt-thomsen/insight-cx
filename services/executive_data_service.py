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

                "top_themes":
                    previous_summary.summary_json.get(
                        "top_themes",
                        []
                    )
            }

        return {

            "metrics": self._get_metrics(),

            "themes": self._get_themes(
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

    def _get_themes(
        self,
        analyses
    ):
        """
        Return the most common themes.
        """

        counter = Counter()

        for analysis in analyses:

            if analysis.themes:

                counter.update(
                    analysis.themes
                )

        return [

            {
                "theme": theme,
                "count": count
            }

            for theme, count
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

            if analysis.emotion:

                counter[
                    analysis.emotion
                ] += 1

        return [

            {
                "emotion": emotion,
                "count": count
            }

            for emotion, count
            in counter.items()

        ]

    def _get_representative_comments(
            self,
            analyses,
    ):
        """
        Return representative comments grouped by theme.
        """

        comments = {}

        for analysis in analyses:

            if (
                    not analysis.feedback
                    or not analysis.themes
            ):
                continue

            for theme in analysis.themes:

                comments.setdefault(
                    theme,
                    []
                )

                # Keep up to three example comments
                if len(comments[theme]) < 3:
                    comments[theme].append({

                        "sentiment": analysis.sentiment,

                        "priority": analysis.priority,

                        "comment": analysis.feedback.comment

                    })

        return comments