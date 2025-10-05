from datetime import datetime

import htpy as h
from flask import url_for
from markupsafe import Markup

from .constants import CET


def base_template(content: h.Element) -> h.Element:
    return h.html(data_theme="light")[
        h.head[
            h.title["Är det dags nu?"],
            h.meta(name="viewport", content="width=device-width,initial-scale=1"),
            h.script(src="https://cdn.jsdelivr.net/npm/simplycountdown.js@1.6.0/dist/simplyCountdown.min.js"),
            h.link(href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css", rel="stylesheet"),
            h.script(src="https://pbutcher.uk/flipdown/js/flipdown/flipdown.js"),
            h.link(href="https://pbutcher.uk/flipdown/css/flipdown/flipdown.css", rel="stylesheet"),
            h.style[
                Markup("""
                    .flipdown {
                        width:100%;
                    }
                    .flipdown .rotor-group .rotor-group-heading::before {
                        font-weight:normal;
                        text-transform: uppercase;
                        font-size:0.8rem;
                        color: #4F4F4F;
                    }
                    """)
            ],
        ],
        h.body[
            h.main(".container", style="min-height:100vh; display:grid; place-items:center")[
                h.article(style="max-width:800px; margin: auto")[content],
            ],
        ],
    ]


def form(heading: str, initial_title: str | None = None) -> h.Element:
    return base_template(
        h.div[
            h.h1[heading],
            h.form(action=url_for("countdown"), method="POST")[
                h.fieldset[
                    h.input(
                        type="text",
                        placeholder="Titel",
                        name="title",
                        required=True,
                        maxlength=100,
                        value=initial_title.capitalize() if initial_title else None,
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


def countdown(heading: str, target: datetime) -> h.Element:
    if target <= datetime.now(CET):
        return base_template(
            h.div[
                h.h1[heading],
                h.p["Det är dags!"],
                h.img(src=f"{url_for('static', filename='done.png')}"),
            ]
        )
    return base_template(
        h.div[
            h.h1[heading],
            h.div("#flipdown.flipdown"),
            h.script[
                Markup(
                    f"""
                    function initFlipDown() {{
                        // Unix timestamp (in seconds) to count down to
                        const twoDaysFromNow = {int(target.timestamp())};

                        // Set up FlipDown
                        const flipdown = new FlipDown(
                            twoDaysFromNow,
                           {{headings: ["Dagar", "Timmar", "Minuter", "Sekunder"]}},
                        ).start().ifEnded(() => {{
                            setTimeout(() => window.location.reload(), 2000);
                        }});
                    }};
                    document.addEventListener('DOMContentLoaded', initFlipDown);
                """
                )
            ],
        ]
    )
