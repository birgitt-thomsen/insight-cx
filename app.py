""" This script handles all flask routes for the application."""
import os
from flask import Flask
from models import db #, Feedback, Analysis
from storage.feedback_storage import FeedbackStorage

app = Flask(__name__)

# Define path to database file
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"sqlite:///{os.path.join(basedir, 'data/insightcx.db')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app.

feedback_storage = FeedbackStorage()

if __name__ == "__main__":
    # One-time creation of database
    # with app.app_context():
    #     db.create_all()

    app.run()
