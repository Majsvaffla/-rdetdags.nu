import os
from datetime import date, datetime, timedelta
from urllib.parse import urljoin

import sentry_sdk
from flask import Flask, make_response, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
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

    @property
    def is_past(self) -> bool:
        return self.date.astimezone(CET) < datetime.now(CET) - timedelta(days=1)  # type: ignore[no-any-return]


# Ensure tables exist
with app.app_context():
    db.create_all()


@app.route("/-/")
def health_check() -> Response:
    return make_response("Tackar som frågar!")


def _slugify(s: str) -> str:
    return s.lower().strip(" -\n\r\t")


def _create_or_edit_countdown(title: str, target: date) -> CountDown:
    slug = _slugify(title)
    if (cd := CountDown.query.filter_by(slug=slug).first()) and cd.is_past:
        cd.date = target
        db.session.add(cd)
        db.session.commit()
        return cd  # type: ignore[no-any-return]

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

        target = datetime.fromisoformat(data["dt"]).astimezone(CET)
        if target < datetime.now(CET):
            return _make_bad_request_response()

        cd = _create_or_edit_countdown(data["title"], target)

        return redirect(urljoin(url_for("countdown"), cd.slug), code=301)

    assert request.method == "GET"

    if not slug:
        return make_response(str(components.form()))

    cd = CountDown.query.filter_by(slug=_slugify(slug)).first()
    if not cd or cd.is_past:
        return make_response(str(components.form(escape(slug))), 404)

    return make_response(str(components.countdown(heading=escape(cd.title), target=cd.date.astimezone(CET))))
