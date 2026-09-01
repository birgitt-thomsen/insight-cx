"""
Converts existing SQLAlchemy models and service return values into
JSON-serializable dictionaries for the API layer.

This module contains no business logic. It only reshapes data that is
already produced by the existing storage/service layer so the frontend
can consume it as JSON.
"""


def serialize_feedback(feedback, include_analysis=True):
    """Serialize a Feedback record, optionally with its latest analysis."""

    if feedback is None:
        return None

    data = {
        "id": feedback.id,
        "customer_name": feedback.customer_name,
        "customer_id": feedback.customer_id,
        "order_number": feedback.order_number,
        "comment": feedback.comment,
        "survey_type": feedback.survey_type,
        "score": feedback.score,
        "nps_category": feedback.nps_category,
        "csat_category": feedback.csat_category,
        "source": feedback.source,
        "feedback_date": (
            feedback.feedback_date.isoformat()
            if feedback.feedback_date else None
        ),
        "uploaded_at": (
            feedback.uploaded_at.isoformat()
            if feedback.uploaded_at else None
        ),
        "is_test_sample": feedback.is_test_sample,
    }

    if include_analysis:
        data["analysis"] = serialize_analysis(feedback.latest_analysis)

    return data


def serialize_analysis(analysis):
    """Serialize an Analysis record."""

    if analysis is None:
        return None

    return {
        "id": analysis.id,
        "feedback_id": analysis.feedback_id,
        "sentiment": analysis.sentiment,
        "emotions": analysis.emotions,
        "intent": analysis.intent,
        "priority": analysis.priority,
        "confidence_score": analysis.confidence_score,
        "confidence_level": analysis.confidence_level,
        "reason_codes": analysis.reason_codes,
        "business_signal": analysis.business_signal,
        "analysis_json": analysis.analysis_json,
        "model": analysis.model,
        "system_prompt_version": analysis.system_prompt_version,
        "feedback_prompt_version": analysis.feedback_prompt_version,
        "analysis_version": analysis.analysis_version,
        "analyzed_at": (
            analysis.analyzed_at.isoformat()
            if analysis.analyzed_at else None
        ),
    }


def serialize_feedback_page(pagination):
    """Serialize a Flask-SQLAlchemy Pagination object of Feedback records."""

    return {
        "items": [serialize_feedback(item) for item in pagination.items],
        "page": pagination.page,
        "pages": pagination.pages,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
        "next_page": pagination.next_num,
        "prev_page": pagination.prev_num,
    }


def serialize_ai_settings(settings):
    """Serialize the singleton AISettings row."""

    if settings is None:
        return None

    return {
        "feedback_model": settings.feedback_model,
        "feedback_temperature": settings.feedback_temperature,
        "system_prompt_version": settings.system_prompt_version,
        "feedback_prompt_version": settings.feedback_prompt_version,
        "executive_model": settings.executive_model,
        "executive_temperature": settings.executive_temperature,
        "executive_prompt_version": settings.executive_prompt_version,
        "description": settings.description,
        "updated_at": (
            settings.updated_at.isoformat()
            if settings.updated_at else None
        ),
    }


def serialize_executive_insight(insight):
    """Serialize an ExecutiveInsights record."""

    if insight is None:
        return None

    return {
        "id": insight.id,
        "summary": insight.summary_json,
        "model": insight.model,
        "system_prompt_version": insight.system_prompt_version,
        "executive_prompt_version": insight.executive_prompt_version,
        "generated_at": (
            insight.generated_at.isoformat()
            if insight.generated_at else None
        ),
    }


def serialize_prompt_test_run(result):
    """
    Serialize the dict returned by AnalysisService.test_feedback()
    or AnalysisService.test_sample().
    """

    return {
        "total": result["total"],
        "successful": result["successful"],
        "failed": result["failed"],
        "statistics": result["statistics"],
        "failures": result["failures"],
        "results": [
            serialize_prompt_test_item(item)
            for item in result["results"]
        ],
    }


def serialize_prompt_test_item(item):
    """Serialize a single per-feedback item from a prompt test run."""

    return {
        "feedback": serialize_feedback(item["feedback"], include_analysis=False),
        "current": serialize_analysis(item["current"]),
        "output": item["output"],
        "error": item["error"],
        "changed_fields": item["changed_fields"],
    }


def serialize_latest_benchmark(latest_benchmark):
    """Serialize the dict returned by BenchmarkService.get_latest_benchmark()."""

    if latest_benchmark is None:
        return None

    completed_at = latest_benchmark.get("completed_at")

    return {
        "completed_at": completed_at.isoformat() if completed_at else None,
        "feedback_count": latest_benchmark.get("feedback_count"),
    }
