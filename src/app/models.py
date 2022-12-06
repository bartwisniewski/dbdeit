# File for your models

from . import db


class Exercise(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    exercise_type = db.Column(db.Integer, default=9)
    categories = db.Column(db.String(255))
    level = db.Column(db.String(50))
    words = db.relationship("ExerciseWord", backref='exercise', lazy=True)
    options = db.relationship("ExerciseOption", backref='exercise', lazy=True)
    sentences = db.relationship("ExerciseSentence", backref='exercise', lazy=True)
    externs = db.relationship("ExerciseExtern", backref='exercise', lazy=True)
    entries = db.relationship("BlogEntry", backref='exercise', lazy=True)

    def __init__(self, title, exercise_type, categories, level):
        self.title, self.exercise_type, self.categories, self.level = title, exercise_type, categories, level

    def get_id(self):
        return self._id

    @staticmethod
    def query_exercises_ids(query):
        exercises_queryset = Exercise.query.filter((Exercise.title.contains(query))
                                                        | (Exercise.categories.contains(query))
                                                        | (Exercise.level.contains(query)))
        exercises = db.session.scalars(exercises_queryset).all()
        exercises_ids = [exercise.get_id() for exercise in exercises]
        return exercises_ids


class Word(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(80), unique=True)
    translation = db.Column(db.String(80))
    preposition = db.Column(db.String(10))
    variant = db.Column(db.String(255))
    exercises = db.relationship("ExerciseWord", backref='word', lazy=True)


class ExerciseWord(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise._id"), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey("word._id"), nullable=False)


class ExerciseOption(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise._id"), nullable=False)
    name = db.Column(db.String(80))
    value = db.Column(db.Integer, default=0)


class ExerciseSentence(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise._id"), nullable=False)
    sentence = db.Column(db.String(150))
    mark = db.Column(db.Integer, default=0)
    gap = db.Column(db.Integer, default=1)


class ExerciseExtern(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise._id"), nullable=False)
    code = db.Column(db.Text)


class BlogEntry(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    subtitle = db.Column(db.String(120))
    picture_path = db.Column(db.String(255))
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise._id"), nullable=True)
    entry_text = db.Column(db.Text)
    author = db.Column(db.String(80))
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, onupdate=db.func.now())

    def get_id(self):
        return self._id

    @staticmethod
    def query_entries(query):
        if query and len(query) >= 2:
            exercises_ids = Exercise.query_exercises_ids(query)
            queryset = BlogEntry.query.filter((BlogEntry.title.contains(query))
                                       | (BlogEntry.subtitle.contains(query))
                                       | (BlogEntry.entry_text.contains(query))
                                       | (BlogEntry.exercise_id.in_(exercises_ids)))
        else:
            queryset = BlogEntry.query
        return queryset.order_by(BlogEntry._id.desc())
