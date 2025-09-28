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


CET = zoneinfo.ZoneInfo("Europe/Stockholm")


def _base_template(content: h.Element) -> str:
    return str(
        h.html[
            h.head[
                h.title["Är det dags nu?"],
                h.script(src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.7/dist/htmx.min.js"),
                h.script(src="https://cdn.jsdelivr.net/npm/simplycountdown.js@1.6.0/dist/simplyCountdown.min.js"),
                h.link(
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css",
                    rel="stylesheet",
                ),
                h.style[
                    Markup("""
                        #countdown {
                            display: flex;
                            justify-content: center;
                            gap: 1rem;
                            font-family: Arial, sans-serif;
                        }
                        #countdown .simply-days,
                        #countdown .simply-hours,
                        #countdown .simply-minutes,
                        #countdown .simply-seconds {
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                        }
                    """)
                ],
            ],
            h.body[
                h.main(".d-flex.justify-content-center.align-items-center.min-vh-100")[
                    h.div(
                        ".card.shadow-lg.p-4",
                        style="max-width: 500px; width: 100%;",
                    )[content],
                ],
            ],
        ]
    )


@app.route("/")
def home():
    return make_response(
        _base_template(
            h.div[
                h.h1(".h4.text-center.mb-4")["Är det dags nu?"],
                h.form(
                    hx_post="/countdown",
                    hx_target="this",
                    hx_swap="outerHTML",
                )[
                    h.div(".mb-3")[
                        h.input(
                            ".form-control",
                            placeholder="Titel",
                            name="title",
                            required=True,
                        ),
                        h.input(
                            ".form-control.mt-3",
                            type="datetime-local",
                            name="dt",
                            required=True,
                        ),
                    ],
                    h.div(".text-center")[h.button(".btn.btn-primary.mt-2", type="submit")["Dags?"],],
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
        _base_template(
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
