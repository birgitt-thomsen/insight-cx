""" This script handles all flask routes for the application."""
import os
from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
from models import db
from storage.feedback_storage import FeedbackStorage
from services.csv_importer import CSVImporter
from storage.dashboard_storage import DashboardStorage
from services.ai_service import AIService

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
ai = AIService()

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
    """ Handle csv upload route. """

    if request.method == "POST":
        try:
            records = csv_importer.import_feedback(
                request.files.get("file")
            )
            feedback_storage.add_feedback(records)
            flash(
                f"Successfully imported {len(records)} feedback records.",
                "success",
            )
        # Show error if raised in csv_importer
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

    return render_template(
        "feedback.html",
        feedback_page=feedback_page
    )

if __name__ == "__main__":
    # One-time creation of database
    # with app.app_context():
    #     db.create_all()

    app.run()
