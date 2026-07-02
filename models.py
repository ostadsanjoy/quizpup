from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    # New Registration fields
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    subscription_status = db.Column(db.String(50), default="Free Tier")

class QuizSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False) # easy, medium, hard, god mode
    total_questions = db.Column(db.Integer, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    hints_remaining = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, default=0)
    recommendation = db.Column(db.Text, nullable=True)
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    questions = db.relationship('QuizQuestion', backref='session', lazy=True)

class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('quiz_session.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_1 = db.Column(db.String(255), nullable=False)
    option_2 = db.Column(db.String(255), nullable=False)
    option_3 = db.Column(db.String(255), nullable=False)
    option_4 = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False) # 1, 2, 3, or 4
    hint = db.Column(db.Text, nullable=True)
    explanation = db.Column(db.Text, nullable=True) # Post-attempt feedback structure
    user_answer = db.Column(db.Integer, nullable=True)