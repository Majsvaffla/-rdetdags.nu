from __future__ import annotations

from dataclasses import dataclass
from datetime import date as Date, datetime as DateTime, time as Time, timedelta as TimeDelta
from typing import TYPE_CHECKING, Final

from dax.constants import CET

if TYPE_CHECKING:
    from collections.abc import Callable

    type DatetimeGetter = Callable[[], DateTime]


@dataclass
class Yearly:
    month: int
    day: int
    time: Time | None = None

    def __call__(self) -> DateTime:
        assert 1 <= self.month <= 12
        assert 1 <= self.day <= 31
        now = DateTime.now(CET)
        this_years_target = DateTime.combine(
            date=Date(now.year, self.month, self.day), time=self.time or Time(), tzinfo=CET
        )
        if now >= this_years_target:
            return DateTime(now.year + 1, self.month, self.day, tzinfo=CET)
        return this_years_target


@dataclass
class Weekly:
    weekday: int
    time: Time | None = None

    def __call__(self) -> DateTime:
        assert 1 <= self.weekday <= 7
        now = DateTime.combine(date=DateTime.now(tz=CET).date(), time=self.time or Time(), tzinfo=CET)
        current_weekday = now.isoweekday()
        if current_weekday == self.weekday and DateTime.now(CET) < now:
            return now
        elif current_weekday < self.weekday:
            return now + TimeDelta(days=self.weekday - current_weekday)
        return now + TimeDelta(days=7 - (current_weekday - self.weekday))


COUNTDOWNS: Final[dict[str, DatetimeGetter]] = {
    "julafton": Yearly(12, 24),
    "nyår": Yearly(1, 1),
    "kanelbullens dag": Yearly(10, 4),
    "pizzaonsdag": Weekly(3, Time(12)),
    "löpartorsdag": Weekly(4, Time(12)),
}
