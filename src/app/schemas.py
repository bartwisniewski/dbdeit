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


class ExerciseExternSchema(ma.Schema):
    _id = fields.fields.Integer()
    code = fields.fields.Str()


class ExerciseOptionSchema(ma.Schema):
    _id = fields.fields.Integer()
    name = fields.fields.Str()
    value = fields.fields.Integer()


class ExerciseCompleteSchema(ma.Schema):
    _id = fields.fields.Integer()
    title = fields.fields.Str()
    exercise_type = fields.fields.Integer()
    categories = fields.fields.Str()
    level = fields.fields.Str()
    words = fields.fields.List(fields.fields.Nested(WordSchema()), required=False)
    options = fields.fields.List(fields.fields.Nested(ExerciseOptionSchema()), required=False)
    extern = fields.fields.Nested(ExerciseExternSchema(), required=False)


class BlogEntrySchema(ma.Schema):
    _id = fields.fields.Integer()
    title = fields.fields.Str()
    subtitle = fields.fields.Str()
    picture_path = fields.fields.Str()
    entry_text = fields.fields.Str()
    author = fields.fields.Str()
    created = fields.fields.DateTime()
    updated = fields.fields.DateTime()


class BlogEntryWithExerciseSchema(ma.Schema):
    _id = fields.fields.Integer()
    title = fields.fields.Str()
    subtitle = fields.fields.Str()
    picture_path = fields.fields.Str()
    exercise = fields.fields.Nested(ExerciseCompleteSchema(), required=False)
    entry_text = fields.fields.Str()
    author = fields.fields.Str()
    created = fields.fields.DateTime()
    updated = fields.fields.DateTime()
