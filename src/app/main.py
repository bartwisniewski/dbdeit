import json

from flask import request
from flask.views import MethodView

from . import db
from .models import BlogEntry
from .schemas import BlogEntrySchema, BlogEntryWithExerciseSchema
from .pagination import Pagination

PAGE_SIZE = 10

entry_pagination = Pagination(nested_schema=BlogEntrySchema, limit=PAGE_SIZE)
entry_schema = BlogEntryWithExerciseSchema()


class ListBlogEntryApiView(MethodView):

    def make_url_without_page(self) -> str:
        query = request.args.get('query', None)
        base_url = request.base_url
        if query:
            base_url = f"{base_url}?query={query}"
        return base_url

    def get(self) -> str:
        query = request.args.get('query', None)
        page = request.args.get('page', None)
        if page:
            page = int(page)
        queryset = BlogEntry.query_entries(query)
        entry_pagination.paginate_queryset(queryset, page)
        base_url = self.make_url_without_page()
        return_json = entry_pagination.get_json_response(db, base_url)

        return return_json


class GetBlogEntryApiView(MethodView):

    def get(self, id: int) -> str:
        found_entry = db.session.scalars(db.select(BlogEntry).filter_by(_id=id)).first()
        json = entry_schema.jsonify(found_entry)
        return entry_schema.jsonify(found_entry)
