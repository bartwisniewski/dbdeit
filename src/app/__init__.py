# Flask app/db etc. config file

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from hashlib import md5
from datetime import timedelta
from .constants import DB_PATH

db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    encryptor = md5()

    app.permanent_session_lifetime = timedelta(minutes=30)
    app.secret_key = encryptor.digest()
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
    db.init_app(app)
    ma.init_app(app)

    app.debug = True

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    # CORS(app)
    from .main import ListBlogEntryApiView, GetBlogEntryApiView, GetExerciseApiView
    app.add_url_rule('/api/blog/', view_func=ListBlogEntryApiView.as_view(name="api-blog"))
    app.add_url_rule('/api/blog/<int:id>', view_func=GetBlogEntryApiView.as_view(name="api-blog-id"))
    app.add_url_rule('/api/exercise/<int:id>', view_func=GetExerciseApiView.as_view(name="api-exercise-id"))
    return app
