import os
import re
from datetime import datetime
from urllib.parse import urljoin

import sentry_sdk
from flask import Flask, make_response, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from sqlalchemy.orm import validates
from werkzeug.wrappers import Response

from . import components
from .constants import CET

if dsn := os.environ.get("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=dsn,
        send_default_pii=True,
    )

app = Flask(__name__)

# SQLite config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dax.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class CountDown(db.Model):  # type: ignore[name-defined]
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    @validates("title")
    def generate_slug(self, key, value):
        base_slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
        slug = base_slug
        counter = 1
        # ensure uniqueness
        while CountDown.query.filter_by(slug=slug).first() is not None:
            slug = f"{base_slug}-{counter}"
            counter += 1
        self.slug = slug
        return value


# Ensure tables exist
with app.app_context():
    db.create_all()


@app.route("/-/")
def health_check() -> Response:
    return make_response("Tackar som frågar!")


@app.route("/", methods=["GET", "POST"])
@app.route("/<slug>", methods=["GET"])
def countdown(slug: str | None = None) -> Response:
    if request.method == "POST":
        data = request.form
        if not data or "title" not in data or "dt" not in data:
            return make_response("Formuläret måste fyllas i korrekt.", 400)

        title = data["title"]
        date = datetime.fromisoformat(data["dt"])

        new_cd = CountDown(title=title, date=date)
        db.session.add(new_cd)
        db.session.commit()

        return redirect(urljoin(url_for("countdown"), new_cd.slug), code=301)

    assert request.method == "GET"

    if not slug:
        return make_response(str(components.form("När är det dags?")))

    if cd := CountDown.query.filter_by(slug=slug).first():
        return make_response(str(components.countdown(heading=escape(cd.title), target=cd.date.replace(tzinfo=CET))))

    return make_response(str(components.form("När är det dags?", escape(slug))), 404)
