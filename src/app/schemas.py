from __future__ import annotations

from flask_marshmallow import fields
from . import ma


class ExerciseSchema(ma.Schema):
    _id = fields.fields.Integer()
    title = fields.fields.Str()
    exercise_type = fields.fields.Integer()
    categories = fields.fields.Str()
    level = fields.fields.Str()


class WordSchema(ma.Schema):
    _id = fields.fields.Integer()
    word = fields.fields.Str()
    translation = fields.fields.Str()
    preposition = fields.fields.Str()
    variant = fields.fields.Str()


class ExerciseWordSchema(ma.Schema):
    _id = fields.fields.Integer()
    exercise = fields.fields.Nested(ExerciseSchema())
    word = fields.fields.Nested(WordSchema())


class ExerciseExternSchema(ma.Schema):
    _id = fields.fields.Integer()
    code = fields.fields.Str()


class ExerciseOptionSchema(ma.Schema):
    _id = fields.fields.Integer()
    name = fields.fields.Str()
    value = fields.fields.Integer()


class ExerciseSentenceSchema(ma.Schema):
    _id = fields.fields.Integer()
    sentence = fields.fields.Str()
    mark = fields.fields.Integer()
    gap = fields.fields.Integer()


class ExerciseCompleteSchema(ma.Schema):
    _id = fields.fields.Integer()
    title = fields.fields.Str()
    exercise_type = fields.fields.Integer()
    categories = fields.fields.Str()
    level = fields.fields.Str()
    words = fields.fields.List(fields.fields.Nested(ExerciseWordSchema(exclude=("_id", "exercise",))), required=False)
    options = fields.fields.List(fields.fields.Nested(ExerciseOptionSchema(exclude=("_id",))), required=False)
    sentences = fields.fields.List(fields.fields.Nested(ExerciseSentenceSchema(exclude=("_id",))), required=False)
    externs = fields.fields.List(fields.fields.Nested(ExerciseExternSchema(exclude=("_id",)), required=False))


class BlogEntrySchema(ma.Schema):
    _id = fields.fields.Integer()
    title = fields.fields.Str()
    subtitle = fields.fields.Str()
    picture_path = fields.fields.Str()
    exercise_id = fields.fields.Integer()  # fields.fields.Nested(ExerciseCompleteSchema(), required=False)
    entry_text = fields.fields.Str()
    author = fields.fields.Str()
    created = fields.fields.DateTime()
    updated = fields.fields.DateTime()


class BlogEntryWithExerciseSchema(ma.Schema):
    _id = fields.fields.Integer()
    title = fields.fields.Str()
    subtitle = fields.fields.Str()
    picture_path = fields.fields.Str()
    exercise_id = fields.fields.Nested(ExerciseCompleteSchema(), required=False)
    entry_text = fields.fields.Str()
    author = fields.fields.Str()
    created = fields.fields.DateTime()
    updated = fields.fields.DateTime()



