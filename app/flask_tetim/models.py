from flask_tetim import db
from datetime import datetime


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(512), nullable=False)
    caption_ita = db.Column(db.String(512), nullable=False)
    image_file = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    answers = db.relationship('Answer', backref='question', lazy=True)

    def __repr__(self):
        return f"Question('{self.image_file}', '{self.caption}')"


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(16), nullable=False)
    uuid = db.Column(db.String(36), nullable=False)
    real_answer = db.Column(db.Boolean, nullable=False)
    user_answer = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    model = db.Column(db.String(16), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    def __repr__(self):
        return f"Answer ('{self.uuid}', '{self.user_answer}', '{self.real_answer}')"


class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), nullable=False)
    model = db.Column(db.String(32), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    seconds = db.Column(db.Float, nullable=False)
