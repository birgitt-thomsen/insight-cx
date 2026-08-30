"""
Service for benchmarking AI models.

The BenchmarkService orchestrates benchmark runs but does not
directly handle database operations. Database persistence is
delegated to BenchmarkStorage.
"""

import time
from backend.services.ai_service import AIService
from backend.storage.benchmark_storage import BenchmarkStorage

# TEMP TOKEN COST
# Prices are USD per 1 million tokens
MODEL_PRICING = {
    "gpt-5-mini": {
        "input": 0.25,
        "output": 2.00,
    },

    "gpt-4.1-mini": {
        "input": 0.40,
        "output": 1.60,
    },

    "gpt-4o-mini": {
        "input": 0.15,
        "output": 0.60,
    },
}

class BenchmarkService:
    """
    Runs model benchmarks against existing customer feedback.

    The service is responsible for:
        - selecting feedback
        - calling the AI service
        - measuring latency
        - collecting token usage
        - calculating basic benchmark metrics
        - passing results to BenchmarkStorage

    It does not directly create or update database records.
    """

    def __init__(
            self,
            ai_service=None,
            benchmark_storage=None
    ):
        """
        Initialize the benchmark service.

        Optional dependencies make the service easier to test later.
        """

        self.ai_service = (
            ai_service
            or AIService()
        )

        self.storage = (
            benchmark_storage
            or BenchmarkStorage()
        )

    def run_benchmark(
            self,
            feedback_records,
            model,
            system_prompt_version="v1",
            feedback_prompt_version="v1",
            temperature=None
    ):
        """
        Run a benchmark for one AI model.

        Args:
            feedback_records (list):
                Existing Feedback model records to test.

            model (str):
                AI model to benchmark.

            system_prompt_version (str):
                System prompt version to use.

            feedback_prompt_version (str):
                Feedback prompt version to use.

            temperature (float):
                Temperature to use when supported by the model.

        Returns:
            BenchmarkRun:
                The completed benchmark run.
        """

        # ---------------------------------------------------------
        # STEP 1: Create the benchmark run
        # ---------------------------------------------------------

        benchmark = self.storage.create_run(
            model=model,
            system_prompt_version=system_prompt_version,
            feedback_prompt_version=feedback_prompt_version,
            feedback_count=len(feedback_records)
        )

        # ---------------------------------------------------------
        # Variables used to calculate the final benchmark metrics
        # ---------------------------------------------------------

        total_latency = 0
        total_tokens = 0
        total_cost = 0

        # ---------------------------------------------------------
        # STEP 2: Process each feedback record
        # ---------------------------------------------------------

        for feedback in feedback_records:

            try:

                # Start the timer immediately before the API request.
                start_time = time.perf_counter()

                # Run the existing AI analysis without saving it
                # to the normal Analysis table.
                output, usage = (
                    self.ai_service.execute_test_prompt(
                        feedback.comment,
                        model=model,
                        temperature=temperature,
                        system_prompt_version=system_prompt_version,
                        feedback_prompt_version=feedback_prompt_version,
                        return_usage=True
                    )
                )

                # Stop the timer immediately after the API response.
                latency_ms = (
                                     time.perf_counter() - start_time
                             ) * 1000

                # -------------------------------------------------
                # Extract usage information from the OpenAI response
                # -------------------------------------------------

                input_tokens = usage.input_tokens
                output_tokens = usage.output_tokens
                tokens = usage.total_tokens

                # -------------------------------------------------
                # Calculate the estimated cost for this API request
                # -------------------------------------------------

                estimated_cost = self.calculate_cost(
                    model=model,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens
                )

                # -------------------------------------------------
                # Save the individual benchmark result
                # -------------------------------------------------

                self.storage.save_result(
                    benchmark_id=benchmark.id,
                    feedback_id=feedback.id,
                    latency_ms=latency_ms,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    total_tokens=tokens,
                    estimated_cost=estimated_cost,
                    success=True,
                    sentiment=output.get("sentiment")
                )

                # -------------------------------------------------
                # Add this result to the benchmark totals
                # -------------------------------------------------

                total_latency += latency_ms
                total_tokens += tokens
                total_cost += estimated_cost

            except Exception as e:

                # -------------------------------------------------
                # If one feedback item fails, don't lose the entire
                # benchmark.
                # -------------------------------------------------

                print(
                    f"Benchmark failed for feedback "
                    f"{feedback.id}: {e}"
                )

                # Save a failed result so we know the item was tested.
                self.storage.save_result(
                    benchmark_id=benchmark.id,
                    feedback_id=feedback.id,
                    latency_ms=0,
                    input_tokens=0,
                    output_tokens=0,
                    total_tokens=0,
                    estimated_cost=0,
                    success=False,
                    sentiment=None
                )

        # ---------------------------------------------------------
        # STEP 3: Calculate benchmark-level metrics
        # ---------------------------------------------------------

        feedback_count = len(feedback_records)

        if feedback_count > 0:
            average_latency = (
                    total_latency / feedback_count
            )
        else:
            average_latency = 0

        # ---------------------------------------------------------
        # STEP 4: Complete the benchmark run
        #
        # Consistency is temporarily set to None. We'll add the
        # model-agreement calculation once the basic benchmark works.
        # ---------------------------------------------------------

        completed = self.storage.complete_run(
            benchmark_id=benchmark.id,
            average_latency_ms=average_latency,
            total_tokens=total_tokens,
            estimated_cost=total_cost,
            consistency_score=None
        )

        return completed


    def calculate_cost(
            self,
            model,
            input_tokens,
            output_tokens
    ):
        """
        Calculate the estimated API cost for one request.

        Pricing is stored as USD per 1 million tokens.

        Args:
            model (str):
                Model used for the request.

            input_tokens (int):
                Number of input tokens.

            output_tokens (int):
                Number of output tokens.

        Returns:
            float:
                Estimated request cost in USD.
        """

        pricing = MODEL_PRICING.get(model)

        if not pricing:
            raise ValueError(
                f"No pricing configured for model: {model}"
            )

        input_cost = (
                             input_tokens / 1_000_000
                     ) * pricing["input"]

        output_cost = (
                              output_tokens / 1_000_000
                      ) * pricing["output"]

        return input_cost + output_cost

    def compare_models(
            self,
            feedback_records,
            models,
            system_prompt_version="v1",
            feedback_prompt_version="v1",
            temperature=None
    ):
        """
        Run the same benchmark dataset against multiple AI models.

        Each model receives the exact same feedback records and prompt
        configuration so that the results can be compared fairly.

        Args:
            feedback_records (list):
                Existing Feedback records to use for the comparison.

            models (list):
                List of model names to benchmark.

            system_prompt_version (str):
                System prompt version used for all models.

            feedback_prompt_version (str):
                Feedback prompt version used for all models.

            temperature (float):
                Temperature used when supported by the model.

        Returns:
            list:
                Completed BenchmarkRun objects, one for each model.
        """

        benchmark_runs = []

        # ---------------------------------------------------------
        # Run the same feedback dataset through each model.
        # ---------------------------------------------------------

        for model in models:
            print(
                f"Starting benchmark for model: {model}"
            )

            benchmark = self.run_benchmark(
                feedback_records=feedback_records,
                model=model,
                system_prompt_version=system_prompt_version,
                feedback_prompt_version=feedback_prompt_version,
                temperature=temperature
            )

            benchmark_runs.append(benchmark)

            print(
                f"Completed benchmark for model: {model}"
            )

        return benchmark_runs


    def calculate_consistency(self, benchmark_runs):
        """
        Calculate basic sentiment agreement between benchmark models.

        Each benchmark run represents one model processing the same
        feedback dataset.

        For each feedback item, the sentiment returned by each model
        is compared. A model receives one agreement point when its
        sentiment matches the majority sentiment for that feedback.

        Args:
            benchmark_runs (list):
                Completed BenchmarkRun objects for the models being
                compared.

        Returns:
            dict:
                Model-specific agreement scores and overall agreement.
        """

        # ---------------------------------------------------------
        # Build a lookup of sentiments by feedback ID.
        #
        # Structure:
        #
        # {
        #     feedback_id: {
        #         model: sentiment
        #     }
        # }
        # ---------------------------------------------------------

        feedback_sentiments = {}

        for benchmark in benchmark_runs:

            for result in benchmark.results:

                feedback_id = result.feedback_id

                if feedback_id not in feedback_sentiments:
                    feedback_sentiments[feedback_id] = {}

                feedback_sentiments[feedback_id][
                    benchmark.model
                ] = result.sentiment

        # ---------------------------------------------------------
        # Track agreement for each model.
        # ---------------------------------------------------------

        model_agreement = {}

        for benchmark in benchmark_runs:
            model_agreement[benchmark.model] = {
                "agreements": 0,
                "total": 0
            }

        # ---------------------------------------------------------
        # Compare each feedback item's sentiments.
        # ---------------------------------------------------------

        for feedback_id, sentiments in feedback_sentiments.items():

            # Ignore feedback where not all models returned a result.
            if len(sentiments) != len(benchmark_runs):
                continue

            # Count how often each sentiment occurred.
            sentiment_counts = {}

            for sentiment in sentiments.values():

                if sentiment is None:
                    continue

                sentiment_counts[sentiment] = (
                        sentiment_counts.get(sentiment, 0) + 1
                )

            # If no valid sentiments were returned, skip this item.
            if not sentiment_counts:
                continue

            # Find the majority sentiment.
            majority_sentiment = max(
                sentiment_counts,
                key=sentiment_counts.get
            )

            # -----------------------------------------------------
            # Give each model an agreement point if its sentiment
            # matches the majority sentiment.
            # -----------------------------------------------------

            for model, sentiment in sentiments.items():

                model_agreement[model]["total"] += 1

                if sentiment == majority_sentiment:
                    model_agreement[model]["agreements"] += 1

        # ---------------------------------------------------------
        # Convert agreement counts into percentages.
        # ---------------------------------------------------------

        results = {}

        for model, values in model_agreement.items():

            if values["total"] > 0:

                score = (
                                values["agreements"]
                                / values["total"]
                        ) * 100

            else:

                score = 0

            results[model] = {
                "agreement_score": round(score, 2),
                "agreements": values["agreements"],
                "total": values["total"]
            }

        return results


    def get_model_comparison(self):
        """
        Get the latest benchmark metrics for each model.

        Storage provides the performance metrics. The service
        adds the consistency score calculated from the benchmark
        results.
        """

        comparison = (
            self.storage.get_model_comparison()
        )

        # ---------------------------------------------------------
        # Get the BenchmarkRun objects corresponding to the
        # comparison data so consistency can be calculated.
        # ---------------------------------------------------------

        benchmark_runs = []

        for item in comparison:

            run = self.storage.get_run(
                item["benchmark_id"]
            )

            if run:
                benchmark_runs.append(run)

        # ---------------------------------------------------------
        # Calculate sentiment agreement across the models.
        # ---------------------------------------------------------

        consistency = (
            self.calculate_consistency(
                benchmark_runs
            )
        )

        # ---------------------------------------------------------
        # Add the consistency score to each model's dashboard data.
        # ---------------------------------------------------------

        for item in comparison:

            model = item["model"]

            model_consistency = (
                consistency.get(model)
            )

            if model_consistency:
                item["agreement_score"] = (
                    model_consistency["agreement_score"]
                )
            else:
                item["agreement_score"] = 0

        return comparison


    def get_latest_benchmark(self):
        """
        Get information about the most recently completed
        benchmark comparison.
        """

        run = self.storage.get_latest_completed_run()

        if not run:
            return None

        return {
            "completed_at": run.completed_at,
            "feedback_count": run.feedback_count
        }