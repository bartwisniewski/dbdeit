from flask import request, jsonify
from flask.views import MethodView

from . import db
from .models import Exercise, ExerciseWord, ExerciseExtern, ExerciseOption, BlogEntry
from .schemas import ExerciseSchema, WordSchema, ExerciseExternSchema, ExerciseOptionSchema, ExerciseCompleteSchema, \
    BlogEntrySchema, BlogEntryWithExerciseSchema


entry_schema = BlogEntryWithExerciseSchema()
entries_schema = BlogEntrySchema(many=True)


class ListBlogEntryApiView(MethodView):

    def get(self) -> str:
        all_entries = db.session.scalars(db.select(BlogEntry)).all()
        return entries_schema.jsonify(all_entries)

