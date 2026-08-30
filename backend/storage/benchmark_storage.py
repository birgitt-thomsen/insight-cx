"""
This script handles all database storage operations for model
benchmarks by creating and updating benchmark records in the database.

Calculations and API calls will be handled by BenchmarkService.
"""

from datetime import datetime
from backend.models import db, BenchmarkRun, BenchmarkResult, Feedback


class BenchmarkStorage:
    """
    Handles database operations for model benchmarking.

    Benchmarking uses two related tables:

    BenchmarkRun
        Stores information and summary metrics for one complete
        benchmark run.

    BenchmarkResult
        Stores the result of processing one feedback record
        within a benchmark run.

    This class deliberately contains no benchmark calculations.
    It only creates and updates database records.
    """

    def create_run(
            self,
            model,
            system_prompt_version,
            feedback_prompt_version,
            feedback_count
    ):
        """
        Create a new benchmark run.

        A benchmark run represents one complete test of a model
        against a specific dataset and prompt configuration.

        The run starts with a status of 'running'. Summary metrics
        such as latency, token usage, cost, and consistency are
        populated later when the benchmark is completed.

        Args:
            model (str):
                The AI model being tested.

            system_prompt_version (str):
                Version of the system prompt used for the benchmark.

            feedback_prompt_version (str):
                Version of the feedback analysis prompt used.

            feedback_count (int):
                Number of feedback records included in the benchmark.

        Returns:
            BenchmarkRun:
                The newly created and committed benchmark record.
        """

        # Create the parent BenchmarkRun record.
        benchmark = BenchmarkRun(
            model=model,
            system_prompt_version=system_prompt_version,
            feedback_prompt_version=feedback_prompt_version,
            feedback_count=feedback_count,
            status="running"
        )

        # Add the record to the SQLAlchemy session.
        db.session.add(benchmark)

        # Commit so the database assigns an ID.
        db.session.commit()

        return benchmark

    def save_result(
		    self,
		    benchmark_id,
		    feedback_id,
		    latency_ms,
		    input_tokens,
		    output_tokens,
		    total_tokens,
		    estimated_cost,
		    success,
		    sentiment
    ):
	    """
		Save the result of one feedback analysis.

		Validates that the referenced feedback record exists before
		creating the benchmark result.

		Args:
			benchmark_id (int):
				ID of the BenchmarkRun this result belongs to.

			feedback_id (int):
				ID of the Feedback record that was analyzed.

			latency_ms (float):
				API response time in milliseconds.

			input_tokens (int):
				Number of input tokens used.

			output_tokens (int):
				Number of output tokens generated.

			total_tokens (int):
				Total input and output tokens.

			estimated_cost (float):
				Estimated cost of the API request.

			success (bool):
				Whether the analysis completed successfully.

			sentiment (str):
				Sentiment returned by the model.

		Returns:
			BenchmarkResult:
				The newly created benchmark result.

		Raises:
			ValueError:
				If the referenced feedback record does not exist.
		"""

	    # ---------------------------------------------------------
	    # Verify that the feedback record exists.
	    # ---------------------------------------------------------

	    feedback = db.session.get(
		    Feedback,
		    feedback_id
	    )

	    if not feedback:
		    raise ValueError(
			    f"Feedback {feedback_id} not found."
		    )

	    # ---------------------------------------------------------
	    # Create the benchmark result.
	    # ---------------------------------------------------------

	    result = BenchmarkResult(
		    benchmark_id=benchmark_id,
		    feedback_id=feedback_id,
		    latency_ms=latency_ms,
		    input_tokens=input_tokens,
		    output_tokens=output_tokens,
		    total_tokens=total_tokens,
		    estimated_cost=estimated_cost,
		    success=success,
		    sentiment=sentiment
	    )

	    # Add the result to the database session.
	    db.session.add(result)

	    # Commit the new result.
	    db.session.commit()

	    return result

    def complete_run(
            self,
            benchmark_id,
            average_latency_ms,
            total_tokens,
            estimated_cost,
            consistency_score
    ):
        """
        Mark a benchmark run as completed and save its summary metrics.

        The BenchmarkService calculates these metrics. This method
        is responsible only for storing them in the BenchmarkRun record.

        Args:
            benchmark_id (int):
                ID of the benchmark being completed.

            average_latency_ms (float):
                Average API response latency across the benchmark.

            total_tokens (int):
                Total tokens used across all benchmark results.

            estimated_cost (float):
                Estimated total API cost of the benchmark.

            consistency_score (float):
                Basic consistency percentage for the benchmark.

        Returns:
            BenchmarkRun:
                The updated and committed benchmark record.

        Raises:
            ValueError:
                If the requested benchmark does not exist.
        """

        # Retrieve the benchmark that we want to complete.
        benchmark = db.session.get(
            BenchmarkRun,
            benchmark_id
        )

        # Prevent silently updating nothing if an invalid ID is supplied.
        if not benchmark:
            raise ValueError(
                f"BenchmarkRun {benchmark_id} not found."
            )

        # Store the summary metrics calculated by BenchmarkService.
        benchmark.average_latency_ms = average_latency_ms
        benchmark.total_tokens = total_tokens
        benchmark.estimated_cost = estimated_cost
        benchmark.consistency_score = consistency_score

        # Change the lifecycle status from running to completed.
        benchmark.status = "completed"

        # Record when the benchmark finished.
        benchmark.completed_at = datetime.utcnow()

        # Save all changes.
        db.session.commit()

        return benchmark

    def get_model_comparison(self):
	    """
		Get aggregated benchmark metrics for the latest
		completed benchmark run of each model.

		Returns:
			list:
				One dictionary per model containing the main
				benchmark performance metrics.
		"""

	    # ---------------------------------------------------------
	    # Get all completed benchmark runs.
	    #
	    # We use the latest run for each model so that an older
	    # test does not appear alongside a newer test for the
	    # same model.
	    # ---------------------------------------------------------

	    runs = (
		    BenchmarkRun.query
		    .filter_by(status="completed")
		    .order_by(BenchmarkRun.completed_at.desc())
		    .all()
	    )

	    latest_runs = {}

	    for run in runs:

		    # Keep only the newest completed run for each model.
		    if run.model not in latest_runs:
			    latest_runs[run.model] = run

	    # ---------------------------------------------------------
	    # Build the dashboard data.
	    # ---------------------------------------------------------

	    comparison = []

	    for model, run in latest_runs.items():

		    results = run.results

		    # Only use successful benchmark results when calculating
		    # performance metrics.
		    successful_results = [
			    result
			    for result in results
			    if result.success
		    ]

		    result_count = len(successful_results)

		    if result_count > 0:

			    average_latency = (
					    sum(
						    result.latency_ms
						    for result in successful_results
					    )
					    / result_count
			    )

			    average_tokens = (
					    sum(
						    result.total_tokens
						    for result in successful_results
					    )
					    / result_count
			    )

		    else:

			    average_latency = 0
			    average_tokens = 0

		    # -----------------------------------------------------
		    # Add the aggregated metrics for this model.
		    # -----------------------------------------------------

		    comparison.append({
			    "benchmark_id": run.id,
			    "model": model,
			    "feedback_count": run.feedback_count,
			    "successful_tests": result_count,
			    "average_latency_ms": round(
				    average_latency,
				    2
			    ),
			    "average_tokens": round(
				    average_tokens,
				    2
			    ),
			    "total_tokens": run.total_tokens,
			    "estimated_cost": round(
				    run.estimated_cost,
				    6
			    ),
			    "average_cost_per_feedback": round(
				    run.estimated_cost / result_count,
				    6
			    ) if result_count > 0 else 0,

			    "status": run.status,
		    })

	    return comparison

    def get_run(self, benchmark_id):
	    """
		Retrieve a benchmark run by ID.

		Args:
			benchmark_id (int):
				ID of the benchmark run.

		Returns:
			BenchmarkRun or None:
				The requested benchmark run.
		"""

	    return (
		    BenchmarkRun.query
		    .filter_by(id=benchmark_id)
		    .first()
	    )

    def get_latest_completed_run(self):
	    """
		Get the most recently completed benchmark run.

		Returns:
			BenchmarkRun or None:
				The latest completed benchmark run.
		"""

	    return (
		    BenchmarkRun.query
		    .filter_by(status="completed")
		    .order_by(
			    BenchmarkRun.completed_at.desc()
		    )
		    .first()
	    )