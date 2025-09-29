import htpy as h
from markupsafe import Markup


def base_template(content: h.Element) -> str:
    return str(
        h.html(data_theme="light")[
            h.head[
                h.title["Är det dags nu?"],
                h.meta(name="viewport", content="width=device-width,initial-scale=1"),
                h.script(src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.7/dist/htmx.min.js"),
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
    )
