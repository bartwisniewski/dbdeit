import json

from flask import request, jsonify
from flask.views import MethodView

from . import db
from .models import BlogEntry, Exercise
from .schemas import ExerciseSchema, WordSchema, ExerciseExternSchema, ExerciseOptionSchema, ExerciseCompleteSchema, \
    BlogEntrySchema, BlogEntryWithExerciseSchema, Pagination

PAGE_SIZE = 10

entry_pagination = Pagination(nested_schema=BlogEntrySchema, limit=PAGE_SIZE)

entry_schema = BlogEntryWithExerciseSchema()
entries_schema = BlogEntrySchema(many=True)


class ListBlogEntryApiView(MethodView):


    def get(self) -> str:
        query = request.args.get('query', None)
        page = request.args.get('page', None)
        if page:
            page = int(page)
        queryset = BlogEntry.query_entries(query)
        queryset = entry_pagination.paginate_queryset(queryset, page)
        data = db.session.scalars(queryset).all()
        url = request.base_url
        if query:
            url = f"{url}?query={query}"
        return_json = entry_pagination.jsonify(data, url)

        return return_json


class GetBlogEntryApiView(MethodView):

    def get(self, id: int) -> str:
        found_entry = db.session.scalars(db.select(BlogEntry).filter_by(_id=id)).first()
        json = entry_schema.jsonify(found_entry)
        return entry_schema.jsonify(found_entry)
