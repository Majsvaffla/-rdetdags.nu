from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import htpy as h
from flask import url_for

from .constants import CET

if TYPE_CHECKING:
    from collections.abc import Iterable

    from dax import CountDownUIData


def base_template(content: h.Node, extra_actions: Iterable[h.Node] | None = None) -> h.Element:
    return h.html(data_theme="dark")[
        h.head[
            h.title["Är det dags nu?"],
            h.meta(name="viewport", content="width=device-width,initial-scale=1"),
            h.script(src="https://cdn.jsdelivr.net/npm/simplycountdown.js@1.6.0/dist/simplyCountdown.min.js"),
            h.link(href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css", rel="stylesheet"),
            h.script(src="https://pbutcher.uk/flipdown/js/flipdown/flipdown.js"),
            h.link(href="https://pbutcher.uk/flipdown/css/flipdown/flipdown.css", rel="stylesheet"),
            h.script(src=url_for("static", filename="base.js")),
            h.script(src=url_for("static", filename="countdown.js")),
            h.link(href=url_for("static", filename="base.css"), rel="stylesheet"),
        ],
        h.body[
            h.header[
                h.button(
                    "#theme-toggle.custom-btn",
                    data_tooltip="Byt tema",
                    data_placement="bottom",
                )["🌙"],
                h.button(
                    "#fullscreen.custom-btn",
                    onClick="toggleFullScreen()",
                    data_tooltip="Fullskärm",
                    data_placement="bottom",
                )["🖥️"],
                extra_actions,
                h.div("#lepp-panel.lepp-container")[
                    h.div(".lepp-header")[
                        h.strong["Hur mycket Lepp?"],
                        h.button(".close-btn", onClick="toggleLepp()")["×"],
                    ],
                    h.div(".lepp-controls")[
                        h.label(For="lepp-range")[h.span("#lepp-mins")["0"], " minuter"],
                        h.input(
                            type="range",
                            id="lepp-range",
                            min="0",
                            max="120",
                            value="0",
                            step="1",
                            onInput="updateLepp(this.value)",
                        ),
                        h.button(onClick="setLepp()")["Leppa tiden"],
                    ],
                ],
            ],
            h.main[h.div(".container.countdown-container")[content]],
        ],
    ]


def copy_url_button() -> h.Element:
    return h.button(
        "#fullscreen.custom-btn",
        onClick="copyURL()",
        data_tooltip="Kopiera URL",
        data_placement="bottom",
    )["📋"]


def toggle_lepp_button() -> h.Element:
    return h.button(
        "#time-adjust-toggle.custom-btn",
        onClick="toggleLepp()",
        data_tooltip="Lepptid",
        data_placement="bottom",
    )["🏃"]


def form_page(initial_title: str | None = None) -> h.Element:
    return base_template(
        h.div[
            h.h1["När är det dags?"],
            h.form(action=url_for("countdown"), method="POST")[
                h.fieldset[
                    h.input(
                        type="text",
                        placeholder="Titel",
                        name="title",
                        required=True,
                        maxlength=100,
                        value=initial_title,
                    ),
                    h.input(
                        type="datetime-local",
                        name="dt",
                        required=True,
                        # Explicitly use no time zone for formatting purposes.
                        min=datetime.now(CET).replace(tzinfo=None).isoformat(timespec="minutes", sep=" "),
                    ),
                ],
                h.input(type="submit", value="Dags?"),
            ],
        ],
    )


def countdown(heading: str, target: datetime, id: int = 1) -> h.Element:
    return h.article(".countdown-content")[
        h.h1[heading],
        h.div(f"#flipdown_{id}.flipdown", data_target=int(target.timestamp())),
        h.div(".target-date")[h.i[target.strftime("%Y-%m-%d %H:%M")]],
    ]


def countdown_page(heading: str, target: datetime) -> h.Element:
    if target <= datetime.now(CET):
        return base_template(
            h.div[
                h.h1[heading],
                h.p["Det är dags!"],
                h.img(src=f"{url_for('static', filename='done.png')}"),
            ]
        )
    return base_template(
        countdown(heading, target),
        extra_actions=[copy_url_button, toggle_lepp_button],
    )


def countdowns_page(countdowns: Iterable[CountDownUIData]) -> h.Element:
    return base_template(
        (countdown(**cd, id=n) for n, cd in enumerate(countdowns, start=1)),
        extra_actions=[copy_url_button, toggle_lepp_button],
    )
