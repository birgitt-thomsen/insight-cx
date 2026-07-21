""" This script handles all flask routes for the application."""
import os
from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
from models import db, Feedback
from storage.feedback_storage import FeedbackStorage
from storage.dashboard_storage import DashboardStorage
from storage.ai_settings_storage import AISettingsStorage
from storage.analysis_storage import AnalysisStorage
from services.csv_importer import CSVImporter
from services.analysis_service import AnalysisService
from services.prompt_service import PromptService

load_dotenv() #Load variables from .env
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Define path to database file
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"sqlite:///{os.path.join(basedir, 'data/insightcx.db')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app.

csv_importer = CSVImporter()
feedback_storage = FeedbackStorage()
dashboard_storage = DashboardStorage()
analysis_storage = AnalysisStorage()
ai_settings_storage = AISettingsStorage()
analysis_service = AnalysisService()
prompt_service = PromptService()

@app.route('/')
def dashboard():
    """ Display the main dashboard page. """

    metrics = dashboard_storage.get_dashboard_metrics()
    themes = dashboard_storage.get_theme_breakdown()
    sentiments = dashboard_storage.get_sentiment_breakdown()
    return render_template(
        "dashboard.html",
        metrics=metrics,
        themes=themes,
        sentiments=sentiments
    )

@app.route("/upload", methods=["GET", "POST"])
def upload():
    """Handle csv upload route."""

    if request.method == "POST":

        try:
            records = csv_importer.import_feedback(
                request.files.get("file")
            )

            # Save feedback records
            feedback_objects = feedback_storage.add_feedback(
                records
            )

            # Analyze newly imported feedback
            result = analysis_service.analyze_feedback_list(feedback_objects)

            flash(
                f"Successfully imported {len(feedback_objects)} "
                f"feedback records. "
                f"Analyzed {result['processed']} records "
                f"({result['failed']} failed).",
                "success",
            )

        except ValueError as e:
            flash(str(e), "error")

        except Exception:
            db.session.rollback()
            app.logger.exception("CSV import failed")

            flash(
                "An unexpected error occurred.",
                "error",
            )

        return redirect(url_for("upload"))

    return render_template("upload.html")

@app.route("/feedback")
def feedback():
    """ Display the feedback page. """

    page = request.args.get(
        "page",
        default=1,
        type=int
    )

    feedback_page = feedback_storage.get_feedback_page(
        page=page,
        per_page=25
    )

    sample_count = (
        db.session.query(Feedback)
        .filter_by(is_test_sample=True)
        .count()
    )

    return render_template(
        "feedback.html",
        feedback_page=feedback_page,
        sample_count=sample_count,
    )

@app.route("/feedback/<int:feedback_id>")
def feedback_details(feedback_id):
    """Display a single feedback item and its analysis."""

    feedback_record = feedback_storage.get_feedback(feedback_id)

    if feedback_record is None:
        flash("Feedback not found.", "error")
        return redirect(url_for("feedback"))

    analysis = analysis_storage.get_analysis(feedback_id)

    return render_template(
        "feedback_details.html",
        feedback=feedback_record,
        analysis=analysis
    )

@app.route(
    "/feedback/<int:feedback_id>/reanalyze",
    methods=["POST"]
)
def reanalyze_feedback(feedback_id):
    """Re-analyze a single feedback record."""

    try:
        analysis_service.reanalyze(feedback_id)

        flash(
            "Feedback successfully re-analyzed.",
            "success"
        )

    except ValueError as e:
        flash(str(e), "error")

    except Exception:
        app.logger.exception(
            "Failed to re-analyze feedback."
        )

        flash(
            "An unexpected error occurred.",
            "error"
        )

    return redirect(
        url_for(
            "feedback_details",
            feedback_id=feedback_id
        )
    )

@app.route("/admin")
def admin():
    """Display the admin page."""

    settings = ai_settings_storage.get_settings()

    system_versions = prompt_service.get_versions("system")
    feedback_versions = prompt_service.get_versions("feedback")

    return render_template(
        "admin.html",
        settings=settings,
        system_versions=system_versions,
        feedback_versions=feedback_versions,
    )

@app.route(
    "/admin/ai-settings",
    methods=["POST"]
)
def update_ai_settings():
    """Updates the ai_settings table with a new model, system prompt
    and/or feedback prompt version."""

    # Call update_settings to save new model and prompt settings
    ai_settings_storage.update_settings(

        model=request.form["model"],
        system_prompt_version=request.form[
            "system_prompt"
        ],
        feedback_prompt_version=request.form[
            "feedback_prompt"
        ],
    )

    flash(
        "AI settings updated.",
        "success"
    )

    return redirect(
        url_for("admin")
    )

@app.route(
    "/admin/delete-analyses",
    methods=["POST"]
)

def delete_all_analyses():
    """Delete all analyses stored in the database."""

    analysis_storage.delete_all()

    flash(
        "All analyses deleted.",
        "success"
    )

    return redirect(url_for("admin"))

@app.route(
    "/admin/delete-feedback",
    methods=["POST"]
)

def delete_all_feedback():
    """Delete all feedback stored in the database."""

    feedback_storage.delete_all()

    flash(
        "All feedback deleted.",
        "success"
    )

    return redirect(url_for("admin"))

@app.route(
    "/admin/reanalyze",
    methods=["POST"]
)

def reanalyze_all():
    """Re-analyze all feedback records."""

    result = analysis_service.reanalyze_all()

    flash(
        f"Analysis complete. "
        f"{result['processed']} processed, "
        f"{result['failed']} failed.",
        "success"
    )

    return redirect(url_for("admin"))

@app.post("/feedback/<int:feedback_id>/sample")

def toggle_sample(feedback_id):
    """Handles check boxes for testing flag."""

    selected = (
        request.form["selected"]
        == "true"
    )

    feedback_storage.update_test_sample(
        feedback_id,
        selected
    )

    sample_count = (
        Feedback.query
        .filter_by(is_test_sample=True)
        .count()
    )

    return {
        "sample_count": sample_count
    }


if __name__ == "__main__":
    # One-time creation of database
    # with app.app_context():
    #     db.create_all()

    app.run()
