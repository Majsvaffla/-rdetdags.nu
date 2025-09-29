import os
import re
import zoneinfo
from datetime import datetime

import htpy as h
import sentry_sdk
from flask import Flask, make_response, request, url_for
from flask_sqlalchemy import SQLAlchemy
from markupsafe import Markup
from sqlalchemy.orm import validates

from components import base_template

CET = zoneinfo.ZoneInfo("Europe/Stockholm")

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


@app.route("/")
def home():
    return make_response(
        base_template(
            h.div[
                h.h1["Är det dags nu?"],
                h.form(
                    hx_post="/countdown",
                    hx_target="this",
                    hx_swap="outerHTML",
                )[
                    h.fieldset[
                        h.input(
                            placeholder="Titel",
                            name="title",
                            required=True,
                        ),
                        h.input(
                            type="datetime-local",
                            name="dt",
                            required=True,
                        ),
                    ],
                    h.input(type="submit", value="Dags?"),
                ],
            ],
        )
    )


@app.route("/countdown", methods=["POST"])
def countdown():
    data = request.form
    assert data

    title = data["title"]
    date = datetime.fromisoformat(data["dt"])

    new_cd = CountDown(title=title, date=date)
    db.session.add(new_cd)
    db.session.commit()

    resp = make_response("", 200)
    resp.headers["HX-Redirect"] = url_for("get_countdown", slug=new_cd.slug)
    return resp


@app.route("/<slug>", methods=["GET"])
def get_countdown(slug):
    cd = CountDown.query.filter_by(slug=slug).first_or_404()

    return make_response(
        base_template(
            h.div[
                h.h1[f"{cd.title}"],
                h.div("#countdown"),
                h.script[
                    Markup(f"""
                    simplyCountdown('#countdown', {{
                        year: {cd.date.year},
                        month: {cd.date.month},
                        day: {cd.date.day},
                        hours: {cd.date.hour},
                        minutes: {cd.date.minute},
                        seconds: {cd.date.second},
                        words: {{ day: 'dagar', hour: 'timmar', minute: 'minuter', second: 'sekunder' }},
                        inline: true,
                        enableUtc: false,
                        onEnd: function(){{ console.log('Countdown finished!'); }},
                    }});
                """)
                ],
            ]
        )
    )
