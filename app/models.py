from datetime import datetime, date
from app import db

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    frequency = db.Column(db.String(20), nullable=False, default='daily')
    start_date = db.Column(db.Date, default=datetime.utcnow)

    progress_entries = db.relationship(
        'Progress',
        backref='habit',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )


    def __repr__(self):
        return f'<Habit {self.name}>'

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    date = db.Column(db.Date, default=date.today, nullable=False)

    def __repr__(self):
        return f'<Progress {self.habit_id} on {self.date}>'