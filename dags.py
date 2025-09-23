import os

import htpy as h
import sentry_sdk
from flask import Flask, make_response

if dsn := os.environ["SENTRY_DSN"]:
    sentry_sdk.init(
        dsn=dsn,
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
    )

app = Flask(__name__)


@app.route("/")
def hello_world():
    return make_response(
        str(
            h.html[
                h.head[
                    h.title["Är det dags nu?"],
                    h.script(src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.7/dist/htmx.min.js"),
                    h.link(
                        href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css",
                        rel="stylesheet",
                    ),
                ],
                h.body[
                    h.main(".container.pt-5.text-center")[
                        h.h1["Är det dags nu?"],
                        h.div(".mb-3")[
                            h.input(".form-control", type="text"),
                            h.button(".btn.btn-primary")["Ok"],
                        ],
                    ],
                ],
            ]
        )
    )
