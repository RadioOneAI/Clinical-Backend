import os
from dotenv import load_dotenv

# ✅ Load .env immediately (before importing Config)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(root_dir, ".env"))

from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt, cors
from app.routes import register_routes
from app.models import User
from app.utils.responses import fail

# ✅ import CLI command
from app.commands import create_first_admin


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # ✅ register all routes
    register_routes(app)

    # ✅ register CLI command to create first admin
    app.cli.add_command(create_first_admin)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        # ✅ jwt_data["sub"] is a STRING
        sub = jwt_data.get("sub")
        try:
            user_id = int(sub)
        except (TypeError, ValueError):
            return None
        return User.query.get(user_id)

    @jwt.user_lookup_error_loader
    def user_lookup_error(_jwt_header, jwt_data):
        return fail("User not found.", code=404)

    return app