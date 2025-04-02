import datetime
from functools import singledispatch
from itertools import dropwhile, filterfalse
from typing import Generator

from .date_range_utils import date_range
from .default_holiday_utils import global_default_holiday_discriminator
from .holiday_utils import IsHolidayFuncType


@singledispatch
def is_bizday(
    date: datetime.date,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
) -> bool:
    return not is_holiday(date)


@singledispatch
def get_next_bizday(
    date: datetime.date,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
) -> datetime.date:
    return next(dropwhile(is_holiday, date_range(date, include_start=False)))


@singledispatch
def get_prev_bizday(
    date: datetime.date,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
) -> datetime.date:
    return next(dropwhile(is_holiday, date_range(date, include_start=False, step_days=-1)))  # noqa: E501


@singledispatch
def get_n_next_bizday(
    date: datetime.date,
    n: int,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
) -> datetime.date:
    if n == 0:
        if is_holiday(date):
            raise ValueError(f"n=0 but date={date} is holiday")
        return date
    elif n > 0:
        return get_n_next_bizday(get_next_bizday(date, is_holiday), n - 1, is_holiday)  # noqa: E501
    else:
        return get_n_prev_bizday(date, -n, is_holiday)  # noqa: E501


@singledispatch
def get_n_prev_bizday(
    date: datetime.date,
    n: int,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
) -> datetime.date:
    if n == 0:
        if is_holiday(date):
            raise ValueError(f"n=0 but date={date} is holiday")
        return date
    elif n > 0:
        return get_n_prev_bizday(get_prev_bizday(date, is_holiday), n - 1, is_holiday)  # noqa: E501
    else:
        return get_n_next_bizday(date, -n, is_holiday)  # noqa: E501


@singledispatch
def bizday_range(
    start: datetime.date,
    end: datetime.date,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
    *,
    include_start: bool = True,
    include_end: bool = True,
) -> Generator[datetime.date, None, None]:
    yield from filterfalse(
        is_holiday,
        date_range(
            start,
            end,
            include_start=include_start,
            include_end=include_end,
            step_days=1 if start <= end else -1,
        ),
    )


@singledispatch
def count_bizdays(
    start: datetime.date,
    end: datetime.date,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
    *,
    include_start: bool = True,
    include_end: bool = True,
) -> int:
    if start > end:
        return - count_bizdays(end, start, is_holiday, include_end=include_start, include_start=include_end)  # noqa: E501
    bdrange = bizday_range(start, end, is_holiday, include_start=include_start, include_end=include_end)  # noqa: E501
    return sum(1 for _ in bdrange)
