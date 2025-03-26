from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class HabitForm(FlaskForm):
    name = StringField('Habit Name', validators=[DataRequired()])
    frequency = SelectField('Frequency', choices=[('daily', 'Daily'), ('weekly', 'Weekly')])
    submit = SubmitField('Add Habit')
