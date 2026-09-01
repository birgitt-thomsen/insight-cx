"""
Additive JSON API blueprint for the React frontend.

Every route here calls into the existing storage/service layer used by
the current HTML routes in backend/app.py. No model, business logic,
AI service, schema, or benchmark logic is modified or duplicated.
"""

from flask import Blueprint

api_bp = Blueprint("api", __name__, url_prefix="/api")

from backend.api import routes  # noqa: E402,F401  (registers routes on api_bp)
