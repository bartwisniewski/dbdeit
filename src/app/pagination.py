from flask_marshmallow import fields
from flask import Response
from . import ma
from .schemas import BlogEntrySchema


class PaginatedObject:
    def __init__(self, data, url, next, previous, total):
        self.data = data
        self.url = url
        self.next = next
        self.previous = previous
        self.total = total


class PaginatedSchema(ma.Schema):
    url = fields.fields.Url()
    next = fields.fields.Integer()
    previous = fields.fields.Integer()
    total = fields.fields.Integer()

    def __init__(self, nested_schema, *args, **kwargs):
        self._declared_fields['data'] = fields.fields.List(fields.fields.Nested(nested_schema()))
        super().__init__(*args, **kwargs)


class Pagination:

    def __init__(self, nested_schema, limit=10, page=0):
        self.limit = limit
        self.page = page
        self.paginated_object = None
        self.queryset = None
        self.total = None
        self.schema = PaginatedSchema(nested_schema)

    def paginate_queryset(self, queryset, page: int):
        self.total = queryset.count()
        self.queryset = queryset.limit(self.limit)
        self.page = page
        if self.page:
            offset = self.page * self.limit
            self.queryset = queryset.offset(offset)
        return self.queryset

    def get_next_page(self) -> int:
        page = self.page
        if page is None:
            page = 0
        next_offset = (page+1) * self.limit
        if next_offset <= self.total:
            return page + 1
        return None

    def get_prev_page(self) -> int:
        if self.page is None or self.page == 0:
            return None
        return self.page - 1

    @staticmethod
    def page_url(page, base_url) -> str:
        if page:
            param_char = "&" if base_url[-1] != "/" else "?"
            return f"{base_url}{param_char}page={page}"
        return base_url

    def get_json_response(self, db, base_url):
        if not self.queryset:
            return Response("{'error':'Queryset not initialised, server error'}", status=500, mimetype='application/json')
        next = self.get_next_page()
        previous = self.get_prev_page()
        total = self.total
        data = db.session.scalars(self.queryset).all()
        self.paginated_object = PaginatedObject(data, base_url, next, previous, total)
        return self.schema.jsonify(self.paginated_object)
