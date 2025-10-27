from datetime import datetime as DateTime, time as Time
from typing import Any
from zoneinfo import ZoneInfo

import pytest
import time_machine

from dax.constants import CET
from dax.recurring import Weekly, Yearly


def DateTimeCET(*args: Any, tzinfo: ZoneInfo = CET, **kwargs: Any) -> DateTime:
    # error: "datetime" gets multiple values for keyword argument "tzinfo"  [misc]
    return DateTime(*args, **kwargs, tzinfo=tzinfo)  # type: ignore[misc]


@pytest.mark.parametrize(
    ["current_point_in_time", "yearly_month", "yearly_day", "expected_yearly"],
    [
        (DateTimeCET(2025, 10, 25), 12, 24, DateTimeCET(2025, 12, 24)),
        (DateTimeCET(2025, 12, 24), 12, 24, DateTimeCET(2026, 12, 24)),
        (DateTimeCET(2025, 12, 25), 12, 24, DateTimeCET(2026, 12, 24)),
    ],
)
def test_yearly(current_point_in_time: DateTime, yearly_month: int, yearly_day: int, expected_yearly: DateTime) -> None:
    with time_machine.travel(current_point_in_time):
        assert Yearly(yearly_month, yearly_day)() == expected_yearly


@pytest.mark.parametrize(
    ["current_point_in_time", "weekday", "time", "expected_weekly"],
    [
        (DateTimeCET(2025, 10, 27), 3, Time(13, 37), DateTimeCET(2025, 10, 29, 13, 37)),
        (DateTimeCET(2025, 10, 29, 13, 36), 3, Time(13, 37), DateTimeCET(2025, 10, 29, 13, 37)),
        (DateTimeCET(2025, 10, 29, 13, 38), 3, Time(13, 37), DateTimeCET(2025, 11, 5, 13, 37)),
        (DateTimeCET(2025, 10, 30), 3, Time(13, 37), DateTimeCET(2025, 11, 5, 13, 37)),
        (DateTimeCET(2025, 11, 1), 6, Time(12, 34), DateTimeCET(2025, 11, 1, 12, 34)),
    ],
)
def test_weekly(current_point_in_time: DateTime, weekday: int, time: Time, expected_weekly: DateTime) -> None:
    with time_machine.travel(current_point_in_time):
        assert Weekly(weekday, time)() == expected_weekly
