"""
Database models for DelegateAI
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Meeting(db.Model):
    """Meeting record"""
    __tablename__ = 'meetings'

    id = db.Column(db.Integer, primary_key=True)
    zoom_link = db.Column(db.String(500), nullable=False)
    meeting_name = db.Column(db.String(200))
    rep_name = db.Column(db.String(100))

    # Processing status
    status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed
    error_message = db.Column(db.Text)

    # Results
    transcript = db.Column(db.Text)
    analysis = db.Column(db.Text)  # JSON string with analysis results

    # Metadata
    audio_file_path = db.Column(db.String(500))
    duration_seconds = db.Column(db.Integer)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Meeting {self.id}: {self.meeting_name}>'


class Constituent(db.Model):
    """Constituent information"""
    __tablename__ = 'constituents'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(200))
    department = db.Column(db.String(100))
    role = db.Column(db.String(100))  # PhD, Master's, etc.

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Constituent {self.name}>'


class Issue(db.Model):
    """Identified issues from meetings and surveys"""
    __tablename__ = 'issues'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))  # mental_health, housing, funding, etc.
    priority = db.Column(db.String(50))  # high, medium, low

    # Tracking
    mention_count = db.Column(db.Integer, default=1)
    sentiment = db.Column(db.String(50))  # positive, neutral, negative

    # Source
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Issue {self.title}>'
