import htpy as h
from markupsafe import Markup


def base_template(content: h.Element) -> str:
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
