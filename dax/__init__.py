import json
import os
import re
from datetime import date, datetime, timedelta
from unicodedata import normalize
from urllib.parse import urljoin

import sentry_sdk
from flask import Flask, make_response, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from werkzeug.wrappers import Response

from . import components, recurring
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

    @property
    def is_past(self) -> bool:
        return self.date.replace(tzinfo=CET) < datetime.now(CET) - timedelta(days=1)  # type: ignore[no-any-return]


# Ensure tables exist
with app.app_context():
    db.create_all()


@app.route("/-/")
def health_check() -> Response:
    return make_response("Tackar som frågar!")


def _slugify(s: str) -> str:
    normalized = normalize("NFKC", s)
    lowered = re.sub(r"[^\w\s-]", "", normalized.lower())
    return re.sub(r"[-\s]+", "-", lowered).strip("-_")


def _create_or_edit_countdown(title: str, target: date) -> CountDown:
    slug = _slugify(title)
    cd = CountDown.query.filter_by(slug=slug).first()
    if cd and cd.is_past:
        cd.date = target
        db.session.add(cd)
        db.session.commit()
        return cd  # type: ignore[no-any-return]

    if cd and not cd.is_past:
        # cd exists but still counts down, append suffix and create new one
        suffix = 1
        while CountDown.query.filter_by(slug=slug).first() is not None:
            suffix += 1
            slug = f"{slug}-{suffix}"

    new_cd = CountDown(title=title, slug=slug, date=target)
    db.session.add(new_cd)
    db.session.commit()
    return new_cd


def _make_bad_request_response() -> Response:
    return make_response("Formuläret är inte korrekt ifyllt.", 400)


@app.route("/", methods=["GET", "POST"])
@app.route("/<slug>", methods=["GET"])
def countdown(slug: str | None = None) -> Response:
    if request.method == "POST":
        data = request.form
        if not data or "title" not in data or "dt" not in data:
            return _make_bad_request_response()

        try:
            target = datetime.fromisoformat(data["dt"]).replace(tzinfo=CET)
        except ValueError:
            return _make_bad_request_response()

        if target < datetime.now(CET):
            return _make_bad_request_response()

        slug_for_redirect = (
            recurring_slug
            if (recurring_slug := _slugify(data["title"])) in recurring.COUNTDOWNS
            else _create_or_edit_countdown(data["title"], target).slug
        )

        return redirect(urljoin(url_for("countdown"), slug_for_redirect), code=301)

    assert request.method == "GET"

    if not slug:
        return make_response(str(components.form()))

    if get_recurring_target := recurring.COUNTDOWNS.get(slug.lower()):
        return make_response(
            str(
                components.countdown(
                    heading=slug.capitalize(),
                    target=get_recurring_target(),
                )
            )
        )

    cd = CountDown.query.filter_by(slug=_slugify(slug)).first()
    if not cd or cd.is_past:
        return make_response(str(components.form(initial_title=escape(slug).capitalize())), 404)

    return make_response(str(components.countdown(heading=escape(cd.title), target=cd.date.replace(tzinfo=CET))))


def _make_json_response(data: dict | None, status_code: int) -> Response:
    response = make_response("" if data is None else json.dumps(data), status_code)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/api/countdown/<slug>", methods=["GET"])
def api_countdown(slug: str) -> Response:
    cd = CountDown.query.filter_by(slug=_slugify(slug)).first()
    if not cd:
        return _make_json_response(None, 404)
    return _make_json_response({"title": cd.title, "timestamp": cd.date.replace(tzinfo=CET).isoformat()}, 200)
