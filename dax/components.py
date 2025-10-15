from datetime import datetime

import htpy as h
from flask import url_for
from markupsafe import Markup

from .constants import CET


def base_template(content: h.Element) -> h.Element:
    return h.html(data_theme="dark")[
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
                    .hide-cursor {
                        cursor: none;
                    }
                    """)
            ],
        ],
        h.body[
            h.main(".container", style="min-height:100vh; display:grid; place-items:center")[
                h.article(style="max-width:800px; margin: auto")[content],
            ],
            h.div(style="position:absolute;top:0.5rem;left:0.5rem;")[
                h.button(
                    "#theme-toggle",
                    style="background-color:transparent;border:none;box-shadow: none;",
                )["🌙"],
                h.button(
                    "#fullscreen",
                    style="background-color:transparent;border:none;box-shadow: none;",
                    onClick="toggleFullScreen()",
                )["🖥️"],
            ],
            h.script[
                Markup(
                    """
                    const root = document.documentElement;
                    const button = document.getElementById("theme-toggle");

                    const savedTheme = localStorage.getItem("theme");
                    if (savedTheme) {{
                    root.setAttribute("data-theme", savedTheme);
                    }}

                    const updateIcon = () => {{
                    const theme = root.getAttribute("data-theme");
                    button.textContent = theme === "dark" ? "☀️" : "🌙";
                    }};
                    updateIcon();

                    button.addEventListener("click", () => {{
                    const current = root.getAttribute("data-theme");
                    const newTheme = current === "dark" ? "light" : "dark";
                    root.setAttribute("data-theme", newTheme);
                    localStorage.setItem("theme", newTheme);
                    updateIcon();
                    }});

                    function toggleFullScreen() {
                        if ((document.fullScreenElement && document.fullScreenElement !== null) ||
                        (!document.mozFullScreen && !document.webkitIsFullScreen)) {
                            if (document.documentElement.requestFullScreen) {
                                document.documentElement.requestFullScreen();
                            } else if (document.documentElement.mozRequestFullScreen) {
                                document.documentElement.mozRequestFullScreen();
                            } else if (document.documentElement.webkitRequestFullScreen) {
                                document.documentElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);
                            }
                        } else {
                            if (document.cancelFullScreen) {
                                document.cancelFullScreen();
                            } else if (document.mozCancelFullScreen) {
                                document.mozCancelFullScreen();
                            } else if (document.webkitCancelFullScreen) {
                                document.webkitCancelFullScreen();
                            }
                        }
                    }
                """
                )
            ],
        ],
    ]


def form(initial_title: str | None = None) -> h.Element:
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
                           {{headings: ["Dagar", "Timmar", "Minuter", "Sekunder"], theme: "light"}},
                        ).start().ifEnded(() => {{
                            setTimeout(() => window.location.reload(), 2000);
                        }});
                    }};
                    document.addEventListener('DOMContentLoaded', initFlipDown);

                    let hideTimeout;
                    function resetCursorTimer() {{
                    document.body.classList.remove('hide-cursor');
                    clearTimeout(hideTimeout);
                    hideTimeout = setTimeout(() => {{
                        document.body.classList.add('hide-cursor');
                    }}, 2000);
                    }}
                    document.addEventListener('mousemove', resetCursorTimer);
                    resetCursorTimer(); // start timer immediately

                """
                )
            ],
        ]
    )
