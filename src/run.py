# File for starting the project

import os

from app import create_app, db
from app.settings import DB_PATH

app = create_app()


def create_db(app):
    with app.app_context():
        if not os.path.exists(DB_PATH):
            db.create_all()


if __name__ == "__main__":
    create_db(app)
    app.run(host="0.0.0.0", port=5000)
