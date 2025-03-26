from flask import Blueprint, render_template, redirect, url_for, request
from app.models import Habit, Progress
from app.forms import HabitForm
from app import db
from datetime import date, timedelta
from collections import defaultdict

main = Blueprint('main', __name__)

def calculate_stats(habit):
    completions = [entry.date for entry in habit.progress_entries.order_by(Progress.date).all()]
    today = date.today()

    total = len(completions)
    longest_streak = 0
    current_streak = 0
    max_streak = 0
    prev_day = None

    for d in completions:
        if prev_day and (d - prev_day).days == 1:
            current_streak += 1
        else:
            current_streak = 1
        longest_streak = max(longest_streak, current_streak)
        prev_day = d

    # Reset current streak if not done today or yesterday
    if not completions or (today - completions[-1]).days > 1:
        current_streak = 0

    # Completion rate: (# of days with completion / # of days since start)
    days_since_start = (today - habit.start_date).days + 1
    completion_rate = (total / days_since_start) * 100 if days_since_start > 0 else 0

    return {
        'total': total,
        'current_streak': current_streak,
        'longest_streak': longest_streak,
        'completion_rate': round(completion_rate, 1)
    }

@main.route('/', methods=['GET', 'POST'])
def index():
    form = HabitForm()
    if form.validate_on_submit():
        habit = Habit(name=form.name.data, frequency=form.frequency.data)
        db.session.add(habit)
        db.session.commit()
        return redirect(url_for('main.index'))

    habits = Habit.query.all()
    today = date.today()
    stats = {habit.id: calculate_stats(habit) for habit in habits}

    return render_template('index.html', form=form, habits=habits, today=today, stats=stats)


@main.route('/habit/<int:habit_id>/done', methods=['POST'])
def mark_done(habit_id):
    today = date.today()
    # prevent duplicate entries
    existing = db.session.query(Progress).filter_by(habit_id=habit_id, date=today).first()
    if not existing:
        progress = Progress(habit_id=habit_id, date=today)
        db.session.add(progress)
        db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/history')
def history():
    habits = Habit.query.all()
    return render_template('history.html', habits=habits, Progress=Progress)

@main.route('/delete/<int:habit_id>', methods=['POST'])
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    db.session.delete(habit)
    db.session.commit()
    return redirect(url_for('main.index'))

