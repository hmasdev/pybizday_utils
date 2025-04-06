import datetime
from itertools import dropwhile, filterfalse
from typing import Callable, Generator

from .date_range_utils import date_range
from .default_holiday_utils import global_default_holiday_discriminator
from .holiday_utils import IsHolidayFuncType


def is_bizday(
    date: datetime.date | datetime.datetime,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
    *,
    datetime_handler: Callable[[datetime.datetime], datetime.date] = datetime.datetime.date,  # noqa: E501
) -> bool:
    """Check if the given date is a business day.

    Args:
        date (datetime.date | datetime.datetime): date to check.
        is_holiday (IsHolidayFuncType, optional): function to check if a date is a holiday.
            Defaults to global_default_holiday_discriminator.
        datetime_handler (Callable[[datetime.datetime], datetime.date], optional): function to convert
            datetime.datetime to datetime.date. Defaults to datetime.datetime.date.

    Returns:
        bool: True if the date is a business day, False otherwise.
    """  # noqa: E501
    if isinstance(date, datetime.datetime):
        date = datetime_handler(date)
    return not is_holiday(date)


def get_next_bizday(
    date: datetime.date | datetime.datetime,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
    *,
    datetime_handler: Callable[[datetime.datetime], datetime.date] = datetime.datetime.date,  # noqa: E501
) -> datetime.date:
    """Get the next business day after the given date.

    Args:
        date (datetime.date | datetime.datetime): Reference date.
        is_holiday (IsHolidayFuncType, optional): function to check if a date is a holiday.
            Defaults to global_default_holiday_discriminator.
        datetime_handler (Callable[[datetime.datetime], datetime.date], optional): function to convert
            datetime.datetime to datetime.date. Defaults to datetime.datetime.date.

    Returns:
        datetime.date: Next business day after the given date.
    """  # noqa: E501
    if isinstance(date, datetime.datetime):
        date = datetime_handler(date)
    return next(dropwhile(is_holiday, date_range(date, include_start=False)))


def get_prev_bizday(
    date: datetime.date | datetime.datetime,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
    *,
    datetime_handler: Callable[[datetime.datetime], datetime.date] = datetime.datetime.date,  # noqa: E501
) -> datetime.date:
    """Get the previous business day before the given date.

    Args:
        date (datetime.date | datetime.datetime): Reference date.
        is_holiday (IsHolidayFuncType, optional): function to check if a date is a holiday.
            Defaults to global_default_holiday_discriminator.
        datetime_handler (Callable[[datetime.datetime], datetime.date], optional): function to convert
            datetime.datetime to datetime.date. Defaults to datetime.datetime.date.

    Returns:
        datetime.date: Previous business day before the given date.
    """  # noqa: E501
    if isinstance(date, datetime.datetime):
        date = datetime_handler(date)
    return next(dropwhile(is_holiday, date_range(date, include_start=False, step_days=-1)))  # noqa: E501


def get_n_next_bizday(
    date: datetime.date | datetime.datetime,
    n: int,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
    *,
    datetime_handler: Callable[[datetime.datetime], datetime.date] = datetime.datetime.date,  # noqa: E501
) -> datetime.date:
    """Get the n-th next business day after the given date.

    Args:
        date (datetime.date | datetime.datetime): Reference date.
        n (int): Number of business days to skip.
            0 means the same date.
            1 means the next business day.
            -1 means the previous business day.
            n > 1 means the n-th next business day.
            n < -1 means the (-n)-th previous business day.
        is_holiday (IsHolidayFuncType, optional): function to check if a date is a holiday.
            Defaults to global_default_holiday_discriminator.
        datetime_handler (Callable[[datetime.datetime], datetime.date], optional): function to convert
            datetime.datetime to datetime.date. Defaults to datetime.datetime.date.

    Raises:
        ValueError: If n=0 and the date is a holiday.

    Returns:
        datetime.date: n-th next business day after the given date.

    Notes:
        - If n is negative, it will return the (-n)-th previous business day.
    """  # noqa: E501
    if n == 0:
        if is_holiday(date):
            raise ValueError(f"n=0 but date={date} is holiday")
        return date
    elif n > 0:
        return get_n_next_bizday(
            get_next_bizday(date, is_holiday, datetime_handler=datetime_handler),  # noqa: E501
            n - 1,
            is_holiday,
            datetime_handler=datetime_handler,
        )
    else:
        return get_n_prev_bizday(date, -n, is_holiday, datetime_handler=datetime_handler)  # noqa: E501


def get_n_prev_bizday(
    date: datetime.date | datetime.datetime,
    n: int,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
    *,
    datetime_handler: Callable[[datetime.datetime], datetime.date] = datetime.datetime.date,  # noqa: E501
) -> datetime.date:
    """Get the n-th previous business day before the given date."

    Args:
        date (datetime.date | datetime.datetime): Reference date.
        n (int): Number of business days to skip.
            0 means the same date.
            1 means the previous business day.
            -1 means the next business day.
            n > 1 means the n-th previous business day.
            n < -1 means the (-n)-th next business day.
        is_holiday (IsHolidayFuncType, optional): function to check if a date is a holiday.
            Defaults to global_default_holiday_discriminator.
        datetime_handler (Callable[[datetime.datetime], datetime.date], optional): function to convert
            datetime.datetime to datetime.date. Defaults to datetime.datetime.date.

    Raises:
        ValueError: If n=0 and the date is a holiday.

    Returns:
        datetime.date: n-th previous business day before the given date.

    Notes:
        - If n is negative, it will return the (-n)-th next business day.
    """  # noqa: E501
    if n == 0:
        if is_holiday(date):
            raise ValueError(f"n=0 but date={date} is holiday")
        return date
    elif n > 0:
        return get_n_prev_bizday(
            get_prev_bizday(date, is_holiday, datetime_handler=datetime_handler),  # noqa: E501
            n - 1,
            is_holiday,
        )
    else:
        return get_n_next_bizday(date, -n, is_holiday, datetime_handler=datetime_handler)  # noqa: E501


def bizday_range(
    start: datetime.date | datetime.datetime,
    end: datetime.date | datetime.datetime,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
    *,
    include_start: bool = True,
    include_end: bool = True,
    datetime_handler: Callable[[datetime.datetime], datetime.date] = datetime.datetime.date,  # noqa: E501
) -> Generator[datetime.date, None, None]:
    """Generate a range of business days between two dates."

    Args:
        start (datetime.date | datetime.datetime): Start date.
        end (datetime.date | datetime.datetime): End date.
        is_holiday (IsHolidayFuncType, optional): function to check if a date is a holiday.
            Defaults to global_default_holiday_discriminator.
        include_start (bool, optional): Include the start date in the range. Defaults to True.
        include_end (bool, optional): Include the end date in the range. Defaults to True.
        datetime_handler (Callable[[datetime.datetime], datetime.date], optional): function to convert
            datetime.datetime to datetime.date. Defaults to datetime.datetime.date.

    Yields:
        Generator[datetime.date, None, None]: Business days between start and end dates.

    Notes:
        - if include_start is True and start is not a holiday, the start date will be included in the range.
        - if include_end is True and end is not a holiday, the end date will be included in the range.
    """  # noqa: E501
    if isinstance(start, datetime.datetime):
        start = datetime_handler(start)
    if isinstance(end, datetime.datetime):
        end = datetime_handler(end)
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


def count_bizdays(
    start: datetime.date | datetime.datetime,
    end: datetime.date | datetime.datetime,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
    *,
    include_start: bool = True,
    include_end: bool = True,
    datetime_handler: Callable[[datetime.datetime], datetime.date] = datetime.datetime.date,  # noqa: E501
) -> int:
    """Count the number of business days between two dates.

    Args:
        start (datetime.date | datetime.datetime): Start date.
        end (datetime.date | datetime.datetime): End date.
        is_holiday (IsHolidayFuncType, optional): function to check if a date is a holiday.
            Defaults to global_default_holiday_discriminator.
        include_start (bool, optional): Include the start date in the count. Defaults to True.
        include_end (bool, optional): Include the end date in the count. Defaults to True.
        datetime_handler (Callable[[datetime.datetime], datetime.date], optional): function to convert
            datetime.datetime to datetime.date. Defaults to datetime.datetime.date.

    Returns:
        int: Number of business days between start and end dates.

    Notes:
        - if start > end, the count will be negative.
        - if include_start is True and start is not a holiday, the start date will be included in the count.
        - if include_end is True and end is not a holiday, the end date will be included in the count.
    """  # noqa: E501
    if isinstance(start, datetime.datetime):
        start = datetime_handler(start)
    if isinstance(end, datetime.datetime):
        end = datetime_handler(end)
    if start > end:
        return - count_bizdays(end, start, is_holiday, include_end=include_start, include_start=include_end, datetime_handler=datetime_handler)  # noqa: E501
    bdrange = bizday_range(start, end, is_holiday, include_start=include_start, include_end=include_end, datetime_handler=datetime_handler)  # noqa: E501
    return sum(1 for _ in bdrange)
