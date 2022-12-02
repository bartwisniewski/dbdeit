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


class ExerciseCompleteSchema(ma.Schema):
    _id = fields.fields.Integer()
    title = fields.fields.Str()
    exercise_type = fields.fields.Integer()
    categories = fields.fields.Str()
    level = fields.fields.Str()
    words = fields.fields.List(fields.fields.Nested(ExerciseWordSchema(exclude=("_id", "exercise",))), required=False)
    options = fields.fields.List(fields.fields.Nested(ExerciseOptionSchema(exclude=("_id",))), required=False)
    externs = fields.fields.List(fields.fields.Nested(ExerciseExternSchema(exclude=("_id",)), required=False))


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

    def jsonify(self, data, base_url):
        next = self.page_url(self.get_next_page(), base_url)
        previous = self.page_url(self.get_prev_page(), base_url)
        self.paginated_object = Pagination.PaginatedObject(data, next, previous)
        return self.schema.jsonify(self.paginated_object)
