from models import db, Analysis


class AnalysisStorage:
	"""Handles database operations for Analysis records."""

	def get_analysis(self, feedback_id):
		"""Return the analysis for a feedback record."""

		return db.session.query(Analysis).filter_by(
			feedback_id=feedback_id
		).first()

	def save_or_update(
			self,
			feedback_id,
			result,
	):
		"""
        Save a new analysis or update an existing one.
        """

		try:

			analysis_record = (
				db.session.query(Analysis)
				.filter_by(
					feedback_id=feedback_id
				)
				.first()
			)

			if analysis_record is None:

				analysis_record = Analysis(
					feedback_id=feedback_id,
					analysis_version=1
				)

				db.session.add(analysis_record)

			else:

				analysis_record.analysis_version += 1

			analysis = result["analysis"]

			analysis_record.sentiment = analysis["sentiment"]
			analysis_record.emotion = analysis["emotion"]
			analysis_record.themes = analysis["themes"]
			analysis_record.priority = analysis["priority"]
			analysis_record.confidence = analysis["confidence"]
			analysis_record.summary = analysis["summary"]
			analysis_record.analysis_json = analysis

			#
			# Store AI configuration
			#

			analysis_record.model = result["model"]

			analysis_record.system_prompt_version = (
				result["system_prompt_version"]
			)

			analysis_record.feedback_prompt_version = (
				result["feedback_prompt_version"]
			)

			db.session.commit()

			return analysis_record

		except Exception:

			db.session.rollback()

			raise

	def delete_all(self):
		"""Delete every analysis."""

		try:
			Analysis.query.delete()
			db.session.commit()
		except Exception:
			db.session.rollback()
			raise