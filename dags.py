import htpy as h
from flask import Flask, make_response

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
