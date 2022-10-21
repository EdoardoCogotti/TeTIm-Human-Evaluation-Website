from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, StringField
from wtforms.validators import DataRequired, Length


class AnswerForm(FlaskForm):
    real_button = SubmitField('Yes')
    fake_button = SubmitField('No')


class ChooseModelPlayForm(FlaskForm):
    model = SelectField('Models', choices=['Random', 'Woody', 'Igloo', 'Paradise', 'Eva', 'Braid'])
    language = RadioField('Language', choices=['English', 'Italiano'], default='English')
    play_button = SubmitField('Play')


class ChooseModelShowForm(FlaskForm):
    model = SelectField('Models', choices=['Woody', 'Igloo', 'Paradise', 'Eva', 'Braid'])
    show_button = SubmitField('Show')


class SaveScoreForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=2, max=10)])
    submit_button = SubmitField('Save')
