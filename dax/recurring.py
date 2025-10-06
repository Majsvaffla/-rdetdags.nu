from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Final

from dax.constants import CET

if TYPE_CHECKING:
    from collections.abc import Callable

    type DatetimeGetter = Callable[[], datetime]


def julafton() -> datetime:
    now = datetime.now(CET)
    this_years_target = datetime(now.year, 12, 24, tzinfo=CET)
    if now > this_years_target:
        return datetime(now.year + 1, 12, 24, tzinfo=CET)
    return this_years_target


def nyår() -> datetime:
    return datetime(datetime.now(CET).year + 1, 1, 1, tzinfo=CET)


def kanelbullens_dag() -> datetime:
    now = datetime.now(CET)
    this_years_target = datetime(now.year, 10, 4, tzinfo=CET)
    if now > this_years_target:
        return datetime(now.year + 1, 10, 4, tzinfo=CET)
    return this_years_target


COUNTDOWNS: Final[dict[str, DatetimeGetter]] = {
    "julafton": julafton,
    "nyår": nyår,
    "kanelbullens dag": kanelbullens_dag,
}
