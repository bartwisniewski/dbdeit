from flask_marshmallow import fields
from flask import Response
from . import ma


class Pagination:

    class PaginatedObject:
        def __init__(self, data, next, previous):
            self.data = data
            self.next = next
            self.previous = previous

    def __init__(self, nested_schema, limit=10, page=0):
        class PaginatedSchema(ma.Schema):
            next = fields.fields.Url()
            previous = fields.fields.Url()
            data = fields.fields.List(fields.fields.Nested(nested_schema()))
        self.limit = limit
        self.page = page
        self.paginated_object = None
        self.queryset = None
        self.schema = PaginatedSchema()

    def paginate_queryset(self, queryset, page: int):
        self.queryset = queryset.limit(self.limit)
        self.page = page
        if self.page:
            offset = self.page * self.limit
            queryset = queryset.offset(offset)
        return queryset

    def get_next_page(self) -> int:
        count = self.queryset.count()
        page = self.page
        if page is None:
            page = 0
        next_offset = (page+1) * self.limit
        if next_offset <= count:
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
        next = self.page_url(self.get_next_page(), base_url)
        previous = self.page_url(self.get_prev_page(), base_url)
        data = db.session.scalars(self.queryset).all()
        self.paginated_object = Pagination.PaginatedObject(data, next, previous)
        return self.schema.jsonify(self.paginated_object)
