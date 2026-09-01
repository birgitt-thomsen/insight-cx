"""
JSON API routes for the React frontend.

These routes are purely additive: every route below reuses the exact
same storage/service objects as the existing HTML routes in
backend/app.py. No business logic, model, AI service, schema, or
benchmark logic is duplicated or changed here - this module only
adapts existing return values into JSON responses.

The existing HTML routes in backend/app.py are untouched and continue
to work exactly as before.
"""

from flask import request, jsonify
from backend.models import db, Feedback
from backend.api import api_bp
from backend.api.serializers import (
    serialize_feedback,
    serialize_feedback_page,
    serialize_ai_settings,
    serialize_executive_insight,
    serialize_prompt_test_run,
    serialize_latest_benchmark,
)
from backend.storage.feedback_storage import FeedbackStorage
from backend.storage.ai_settings_storage import AISettingsStorage
from backend.storage.analysis_storage import AnalysisStorage
from backend.storage.executive_insights_storage import ExecutiveInsightsStorage
from backend.services.benchmark_service import BenchmarkService
from backend.services.csv_importer import CSVImporter
from backend.services.analysis_service import AnalysisService
from backend.services.prompt_service import PromptService
from backend.services.executive_data_service import ExecutiveDataService
from backend.services.executive_summary_service import ExecutiveSummaryService

csv_importer = CSVImporter()
feedback_storage = FeedbackStorage()
analysis_storage = AnalysisStorage()
ai_settings_storage = AISettingsStorage()
executive_storage = ExecutiveInsightsStorage()
analysis_service = AnalysisService()
prompt_service = PromptService()
executive_data_service = ExecutiveDataService()
executive_summary_service = ExecutiveSummaryService()


# ---------------------------------------------------------------------
# EXECUTIVE BRIEF
# ---------------------------------------------------------------------

@api_bp.get("/executive-summary/latest")
def api_executive_summary_latest():
    """Return the latest and previous executive summaries."""

    latest = executive_storage.get_latest_summary()
    previous = executive_storage.get_previous_summary()

    priority_counts = {}

    if latest and latest.summary_json:

        for action in latest.summary_json.get("recommended_actions", []):

            for priority in action.get("supports_priority", []):
                priority_counts[priority] = priority_counts.get(priority, 0) + 1

    return jsonify({
        "latest": serialize_executive_insight(latest),
        "previous": serialize_executive_insight(previous),
        "priority_counts": priority_counts,
    })


@api_bp.post("/executive-summary/generate")
def api_executive_summary_generate():
    """Generate and persist a new executive summary."""

    body = request.get_json(silent=True) or {}

    model = body.get("model") or None

    try:
        summary_data = executive_data_service.build_summary_data()

        result = executive_summary_service.generate_summary(
            summary_data,
            model=model,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(result)


# ---------------------------------------------------------------------
# FEEDBACK EXPLORER
# ---------------------------------------------------------------------

@api_bp.get("/feedback")
def api_feedback_list():
    """Return a paginated, filterable list of feedback records."""

    page = request.args.get("page", default=1, type=int)

    filters = {
        "search": request.args.get("search", default="", type=str),
        "survey_type": request.args.get("survey_type", default="", type=str),
        "sentiment": request.args.get("sentiment", default="", type=str),
        "priority": request.args.get("priority", default="", type=str),
    }

    feedback_page = feedback_storage.get_feedback_page(
        page=page, per_page=25, filters=filters
    )

    sample_count = db.session.query(Feedback).filter_by(is_test_sample=True).count()

    survey_types = (
        db.session.query(Feedback.survey_type)
        .distinct()
        .order_by(Feedback.survey_type)
        .all()
    )

    survey_types = [row[0] for row in survey_types if row[0]]

    response = serialize_feedback_page(feedback_page)
    response["sample_count"] = sample_count
    response["survey_types"] = survey_types

    return jsonify(response)


@api_bp.get("/feedback/test-sample")
def api_feedback_test_sample():
    """Return the feedback records currently flagged for benchmark testing."""

    records = feedback_storage.get_test_sample()

    return jsonify({
        "items": [serialize_feedback(f) for f in records],
    })


@api_bp.get("/feedback/<int:feedback_id>")
def api_feedback_detail(feedback_id):
    """Return a single feedback record with its analysis."""

    feedback = feedback_storage.get_feedback(feedback_id)

    if feedback is None:
        return jsonify({"error": "Feedback not found."}), 404

    return jsonify(serialize_feedback(feedback))


@api_bp.post("/feedback/<int:feedback_id>/sample")
def api_feedback_toggle_sample(feedback_id):
    """Toggle whether a feedback record is included in the benchmark sample."""

    body = request.get_json(silent=True) or {}

    selected = bool(body.get("selected"))

    feedback_storage.update_test_sample(feedback_id, selected)

    sample_count = db.session.query(Feedback).filter_by(is_test_sample=True).count()

    return jsonify({"sample_count": sample_count})


@api_bp.post("/feedback/<int:feedback_id>/reanalyze")
def api_feedback_reanalyze(feedback_id):
    """Re-analyze a single feedback record and return the updated result."""

    try:
        feedback = analysis_service.reanalyze(feedback_id)

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(serialize_feedback(feedback))


# ---------------------------------------------------------------------
# UPLOAD
# ---------------------------------------------------------------------

@api_bp.post("/upload")
def api_upload():
    """Import a CSV file of feedback records and analyze the new rows."""

    try:
        records = csv_importer.import_feedback(request.files.get("file"))

        feedback_objects = feedback_storage.add_feedback(records)

        result = analysis_service.analyze_feedback_list(feedback_objects)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred."}), 500

    return jsonify({
        "imported": len(feedback_objects),
        "processed": result["processed"],
        "failed": result["failed"],
    })


# ---------------------------------------------------------------------
# AI SETTINGS / ADMINISTRATION
# ---------------------------------------------------------------------

@api_bp.get("/ai-settings")
def api_ai_settings_get():
    """Return current AI settings and available prompt versions."""

    settings = ai_settings_storage.get_settings()

    return jsonify({
        "settings": serialize_ai_settings(settings),
        "prompt_versions": {
            "system": prompt_service.get_versions("system"),
            "feedback": prompt_service.get_versions("feedback"),
            "executive": prompt_service.get_versions("executive"),
        },
    })


@api_bp.post("/ai-settings/feedback")
def api_ai_settings_update_feedback():
    """Update the feedback analysis AI configuration."""

    body = request.get_json(silent=True) or {}

    try:
        settings = ai_settings_storage.update_feedback_settings(
            feedback_model=body["model"],
            feedback_temperature=float(body["temperature"]),
            system_prompt_version=body["system_prompt"],
            feedback_prompt_version=body["feedback_prompt"],
            description=body.get("description"),
        )

    except (KeyError, ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid settings payload: {e}"}), 400

    return jsonify(serialize_ai_settings(settings))


@api_bp.post("/ai-settings/executive")
def api_ai_settings_update_executive():
    """Update the executive summary AI configuration."""

    body = request.get_json(silent=True) or {}

    try:
        settings = ai_settings_storage.update_executive_settings(
            executive_model=body["executive_model"],
            executive_temperature=float(body["executive_temperature"]),
            executive_prompt_version=body["executive_prompt"],
            description=body.get("description"),
        )

    except (KeyError, ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid settings payload: {e}"}), 400

    return jsonify(serialize_ai_settings(settings))


@api_bp.post("/maintenance/reanalyze-all")
def api_maintenance_reanalyze_all():
    """Re-analyze every feedback record."""

    result = analysis_service.reanalyze_all()

    return jsonify(result)


@api_bp.post("/maintenance/delete-analyses")
def api_maintenance_delete_analyses():
    """Delete all analyses, keeping raw feedback."""

    analysis_storage.delete_all()

    return jsonify({"success": True})


@api_bp.post("/maintenance/delete-feedback")
def api_maintenance_delete_feedback():
    """Delete all feedback and analyses."""

    feedback_storage.delete_all()

    return jsonify({"success": True})


# ---------------------------------------------------------------------
# AI EVALUATION (Single Feedback / Benchmark Lab)
# ---------------------------------------------------------------------

@api_bp.post("/ai-evaluation/single")
def api_ai_evaluation_single():
    """Dry-run a prompt/model configuration against one feedback record."""

    body = request.get_json(silent=True) or {}

    feedback_id = body.get("feedback_id")

    if not feedback_id:
        return jsonify({"error": "feedback_id is required."}), 400

    feedback = feedback_storage.get_feedback(feedback_id)

    if feedback is None:
        return jsonify({"error": "Feedback not found."}), 404

    temperature = body.get("temperature")

    result = analysis_service.test_feedback(
        feedback,
        model=body.get("model"),
        temperature=float(temperature) if temperature is not None else None,
        system_prompt_version=body.get("system_prompt_version"),
        feedback_prompt_version=body.get("feedback_prompt_version"),
    )

    return jsonify(serialize_prompt_test_run(result))


@api_bp.post("/ai-evaluation/benchmark")
def api_ai_evaluation_benchmark():
    """Dry-run a prompt/model configuration against the benchmark sample."""

    body = request.get_json(silent=True) or {}

    temperature = body.get("temperature")

    result = analysis_service.test_sample(
        model=body.get("model"),
        temperature=float(temperature) if temperature is not None else None,
        system_prompt_version=body.get("system_prompt_version"),
        feedback_prompt_version=body.get("feedback_prompt_version"),
    )

    return jsonify(serialize_prompt_test_run(result))


# ---------------------------------------------------------------------
# MODEL COMPARISON / BENCHMARKS
# ---------------------------------------------------------------------

@api_bp.get("/benchmarks/comparison")
def api_benchmarks_comparison():
    """Return the latest model comparison data."""

    benchmark_service = BenchmarkService()

    comparison = benchmark_service.get_model_comparison()
    latest_benchmark = benchmark_service.get_latest_benchmark()

    return jsonify({
        "comparison": comparison,
        "latest_benchmark": serialize_latest_benchmark(latest_benchmark),
    })


@api_bp.post("/benchmarks/run")
def api_benchmarks_run():
    """
    Run a model comparison using the same fixed dataset and model list
    as the existing HTML route (backend/app.py: run_benchmark_comparison).
    """

    benchmark_service = BenchmarkService()

    feedback_records = Feedback.query.limit(5).all()

    models = [
        "gpt-5-mini",
        "gpt-4.1-mini",
        "gpt-4o-mini",
    ]

    benchmark_service.compare_models(
        feedback_records=feedback_records,
        models=models,
        system_prompt_version="v1",
        feedback_prompt_version="v1",
    )

    comparison = benchmark_service.get_model_comparison()
    latest_benchmark = benchmark_service.get_latest_benchmark()

    return jsonify({
        "comparison": comparison,
        "latest_benchmark": serialize_latest_benchmark(latest_benchmark),
    })
