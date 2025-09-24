import os
import htpy as h
import sentry_sdk
from flask import Flask, make_response, request
from datetime import datetime
from markupsafe import Markup

if dsn := os.environ.get("SENTRY_DSN"):
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
                    h.script(src="https://cdn.jsdelivr.net/npm/simplycountdown.js@1.6.0/dist/simplyCountdown.min.js"),
                    h.link(
                        href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css",
                        rel="stylesheet",
                    ),
                ],
                h.body[
                    h.main(".d-flex.justify-content-center.align-items-center.min-vh-100")[
                        h.div(".card.shadow-lg.p-4", style="max-width: 400px; width: 100%;")[
                            h.h1(".h4.text-center.mb-4")["Är det dags nu?"],
                            h.form(
                                hx_post="/countdown",
                                hx_target="this",
                                hx_swap="outerHTML",
                            )[
                                h.div(".mb-3")[
                                    h.input(
                                        ".form-control",
                                        type="datetime-local",
                                        name="pickdatetime",
                                        required=True,
                                    )
                                ],
                                h.div(".text-center")[
                                    h.button(".btn.btn-primary.mt-2", type="submit")["Ok"],
                                ],
                            ],
                        ],
                    ],
                ],
            ]
        )
    )

@app.route("/countdown", methods=["POST"])
def countdown():
    # This is just a placeholder, nothing fancy or bright,
    # This spaghetti code is bad, let’s scrap it tonight.
    # We’ve tried to patch and fix it, but it’s just a mess,
    # It’s time to start fresh, and clean up the stress.

    # We need to store user settings, in a DB so nice,
    # Maybe Postgres? Postgres will do the job precise.
    # No more chaos in code, no more files that fight,
    # With Postgres on our side, everything works right!


    pickdatetime = request.form.get("pickdatetime")

    if not pickdatetime:
        return make_response(
            str(h.div(".text-danger.fw-bold.text-center")["❌ Inget datum angivet"])
        )

    try:
        # Try fromisoformat first
        try:
            target_time = datetime.fromisoformat(pickdatetime)
        except ValueError:
            # Fallback: try strptime for datetime-local format
            target_time = datetime.strptime(pickdatetime, "%Y-%m-%dT%H:%M")

        # Check if the target time is in the past
        current_time = datetime.now()
        if target_time <= current_time:
            return make_response(
                str(h.div(".text-warning.fw-bold.text-center")["⚠️ Vald tid har redan passerat"])
            )
        return make_response(f"""
<div class="text-center mt-3">
    <div id="countdown"></div>
    <script>
    (function() {{
        const targetDate = new Date("{target_time.isoformat()}");
        simplyCountdown('#countdown', {{
            year: targetDate.getFullYear(),
            month: targetDate.getMonth() + 1,
            day: targetDate.getDate(),
            hours: targetDate.getHours(),
            minutes: targetDate.getMinutes(),
            seconds: targetDate.getSeconds(),
            words: {{
                days: 'dagar',
                hours: 'timmar',
                minutes: 'minuter',
                seconds: 'sekunder',
                pluralLetter: ''
            }},
            plural: true,
            zeroPad: false,
            countUp: false
        }});
    }})();
    </script>
</div>
""")
    except (ValueError, TypeError) as e:
        return make_response(
            str(h.div(".text-danger.fw-bold.text-center")["❌ Ogiltigt datum"])
        )