from flask import request, jsonify
from flask.views import MethodView

from . import db
from .models import BlogEntry
from .schemas import ExerciseSchema, WordSchema, ExerciseExternSchema, ExerciseOptionSchema, ExerciseCompleteSchema, \
    BlogEntrySchema, BlogEntryWithExerciseSchema


entry_schema = BlogEntryWithExerciseSchema()
entries_schema = BlogEntrySchema(many=True)


class ListBlogEntryApiView(MethodView):

    def get(self) -> str:
        print(request.args.get('query'))
        all_entries = db.session.scalars(db.select(BlogEntry)).all()
        return entries_schema.jsonify(all_entries)


class GetBlogEntryApiView(MethodView):

    def get(self, id: int) -> str:
        found_entry = db.session.scalars(db.select(BlogEntry).filter_by(_id=id)).first()
        json = entry_schema.jsonify(found_entry)
        return entry_schema.jsonify(found_entry)
