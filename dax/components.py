from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import htpy as h
from flask import url_for
from markupsafe import Markup

from .constants import CET

if TYPE_CHECKING:
    from collections.abc import Iterable


def base_template(content: h.Element, extra_actions: Iterable[h.Element] | None = None) -> h.Element:
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
                        display: flex !important;
                        flex-wrap: nowrap !important;
                        justify-content: center;
                        align-items: center;
                        width: 100%;
                        transform-origin: center;
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
                    .flipdown .rotor-group {
                        flex: 0 0 auto !important;
                    }
                    @media (max-width: 900px) {
                        .flipdown {
                            transform: scale(0.9);
                        }
                    }
                    @media (max-width: 700px) {
                        .flipdown {
                            transform: scale(0.8);
                        }
                    }
                    @media (max-width: 500px) {
                        .flipdown {
                            transform: scale(0.8);
                        }
                    }
                    .countdown-container {
                       min-height:100vh;
                       display:grid;
                       place-items: center;
                    }
                    .countdown-content {
                       max-width:800px;
                       margin: auto;
                    }
                    .countdown-menu {
                       position:absolute;
                       top:0.5rem;
                       left:0.5rem;
                    }
                    .lepp-container {
                        display: none;
                        position: absolute;
                        top: 0.5rem;
                        left: 0.5rem;
                        background: var(--pico-background-color);
                        padding: 1rem;
                        border-radius: 0.5rem;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        min-width: 250px;
                    }
                    .lepp-container.show {
                        display: block;
                    }
                    .lepp-controls {
                        display: flex;
                        flex-direction: column;
                        gap: 0.5rem;
                    }
                    .lepp-header {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 0.5rem;
                    }
                    .close-btn {
                        background: none;
                        border: none;
                        font-size: 1.2rem;
                        cursor: pointer;
                        padding: 0;
                    }
                    .custom-btn {
                        background-color:transparent;
                        border:none;
                        box-shadow: none;
                       filter: grayscale(100%);
                    }
                    .custom-btn:hover {
                       filter: grayscale(0%);
                    }
                    .target-date {
                        text-align:center;
                        margin-top:1rem;
                        font-size:0.8rem;
                        opacity: 0.8;
                    }
                    """)
            ],
        ],
        h.body[
            h.div[
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
            ],
            h.main(".container.countdown-container")[content],
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

                    function copyURL() {
                    navigator.clipboard.writeText(window.location.href)
                        .then(() => {})
                        .catch(err => {
                        console.error("Failed to copy: ", err);
                        });
                    }

                    function toggleLepp() {
                        const panel = document.getElementById('lepp-panel');
                        panel.classList.toggle('show');
                    }

                    function updateLepp(value) {
                        document.getElementById('lepp-mins').textContent = value;
                    }

                """
                )
            ],
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


def countdown(heading: str, target: datetime) -> h.Element:
    return h.article(".countdown-content")[
        h.h1[heading],
        h.div("#flipdown.flipdown"),
        h.div(".target-date")[h.i[target.strftime("%Y-%m-%d %H:%M")]],
        h.script[
            Markup(
                f"""
                    let currentFlipDown = null;
                    let currentTargetTime = {int(target.timestamp())};

                    function initFlipDown() {{
                        // Unix timestamp (in seconds) to count down to
                        const twoDaysFromNow = currentTargetTime;

                        // Set up FlipDown
                        currentFlipDown = new FlipDown(
                            twoDaysFromNow,
                           {{headings: ["Dagar", "Timmar", "Minuter", "Sekunder"], theme: "light"}},
                        ).start().ifEnded(() => {{
                            setTimeout(() => window.location.reload(), 2000);
                        }});
                    }};
                    document.addEventListener('DOMContentLoaded', initFlipDown);

                    function setLepp() {{
                        const leppMinutes = parseInt(document.getElementById('lepp-range').value);
                        if (leppMinutes > 0) {{
                            currentTargetTime -= (leppMinutes * 60);

                            document.getElementById('lepp-range').value = 0;
                            document.getElementById('lepp-mins').textContent = '0';

                            document.getElementById('lepp-panel').classList.remove('show');

                            const container = document.getElementById('flipdown');
                            container.innerHTML = '';

                            currentFlipDown = new FlipDown(
                                currentTargetTime,
                                {{headings: ["Dagar", "Timmar", "Minuter", "Sekunder"], theme: "light"}},
                            ).start().ifEnded(() => {{
                                setTimeout(() => window.location.reload(), 2000);
                            }});
                        }}
                    }}

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
        extra_actions=[copy_url_button(), toggle_lepp_button()],
    )
