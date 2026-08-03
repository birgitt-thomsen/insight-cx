"""This script handles the storage of the executive insights."""

from models import db, ExecutiveInsights

class ExecutiveInsightsStorage:
    """
    Handles storage and retrieval of executive insights.
    """

    def save_summary(
		    self,
		    input_data,
		    summary,
		    config,
    ):
	    """
		Save a generated executive summary.
		"""
	    insight = ExecutiveInsights(

		    input_json=input_data,

		    summary_json=summary,

		    model=config["model"],

		    system_prompt_version=config["system_prompt_version"],

		    executive_prompt_version=config["executive_prompt_version"],

	    )

	    db.session.add(insight)
	    db.session.commit()

		# FOR TESTING ONLY
	    # print("\nSaving to ExecutiveInsights table...")
	    # print(f"Summary keys: {list(summary.keys())}")
	    # print(f"Input keys: {list(input_data.keys())}")

	    return insight

    def get_latest_summary(self):
	    """
		Return the most recently generated summary.
		"""
	    return (

		    ExecutiveInsights.query

		    .order_by(
			    ExecutiveInsights.generated_at.desc()
		    )

		    .first()

	    )

    def get_previous_summary(self):
	    """
	    Return the previous executive summary.

	    Returns None if fewer than two summaries exist.
	    """

	    return (
		    ExecutiveInsights.query
		    .order_by(
			    ExecutiveInsights.generated_at.desc()
		    )
		    .offset(1)
		    .first()
	    )

    def delete_summary(
		    self,
		    summary_id,
    ):
	    """
		Delete a stored summary.
		"""
	    summary = db.session.get(
		    ExecutiveInsights,
		    summary_id
	    )

	    if summary:
		    db.session.delete(summary)

		    db.session.commit()

