""" This script handles the contents of the main dashboard page. """
from sqlalchemy import func
from collections import Counter
from models import db, Feedback, Analysis

class DashboardStorage:

	def get_dashboard_metrics(self):
		""" Return main dashboard metrics. """

		# Feedback count
		total_feedback = Feedback.query.count()

		# NPS count
		total_nps = Feedback.query.filter_by(
			survey_type="NPS"
		).count()

		# Avg NPS
		avg_nps = db.session.query(
			# Set to 0 when no NPS values
			func.coalesce(func.avg(Feedback.score), 0)
		).filter_by(
			survey_type="NPS"
		).scalar()

		# CSAT count
		total_csat = Feedback.query.filter_by(
			survey_type="CSAT"
		).count()

		# Avg CSAT
		avg_csat = db.session.query(
			# Set to 0 when no CSAT values
			func.coalesce(func.avg(Feedback.score), 0)
		).filter_by(
			survey_type="CSAT"
		).scalar()

		return {
			"feedback_count": total_feedback,
			"nps_count": total_nps,
			"csat_count": total_csat,
			"avg_nps": round(avg_nps, 1),
			"avg_csat": round(avg_csat, 1)
		}

	def get_theme_breakdown(self):
		""" Return theme breakdown. """

		analyses = Analysis.query.all()

		# Create counter for each theme
		counter = Counter()

		for analysis in analyses:
			if analysis.themes:
				counter.update(analysis.themes)

		return counter.most_common(5)

	def get_sentiment_breakdown(self):
		"""Return sentiment breakdown with percentages."""

		analyses = Analysis.query.all()

		counter = Counter()

		for analysis in analyses:
			if analysis.sentiment:
				counter[analysis.sentiment.lower()] += 1

		total = sum(counter.values())

		sentiments = []

		colors = {
			"positive": "green",
			"mixed": "yellow",
			"negative": "red"
		}

		for sentiment, count in counter.items():
			percentage = round((count / total) * 100, 1) if total else 0

			sentiments.append({
				"label": sentiment.capitalize(),
				"count": count,
				"percentage": percentage,
				"color": colors.get(sentiment, "gray")
			})

		return sentiments

