import datetime
from itertools import count
from typing import Callable, Generator


def date_range(
    start: datetime.date | datetime.datetime,
    end: datetime.date | datetime.datetime | None = None,
    *,
    include_start: bool = True,
    include_end: bool = True,
    step_days: int = 1,
    datetime_handler: Callable[[datetime.datetime], datetime.date] = datetime.datetime.date,  # noqa: E501
) -> Generator[datetime.date, None, None]:
    """date generator from start to end.

    Args:
        start (datetime.date | datetime.datetime): start date
        end (datetime.date | datetime.datetime | None, optional): end date. Defaults to None.
        include_start (bool, optional): include start date. Defaults to True.
        include_end (bool, optional): include end date. Defaults to True.
        step_days (int, optional): step days. Defaults to 1
        datetime_handler (Callable[[datetime.datetime], datetime.date], optional): function to convert
            datetime.datetime to datetime.date. Defaults to datetime.datetime.date.

    Yields:
        Generator[datetime.date, None, None]: date generator

    Raises:
        ValueError: step_days is 0
        TypeError: If start or end is not a datetime.date or datetime.datetime object.
    """  # noqa: E501
    if not isinstance(start, (datetime.date, datetime.datetime)):
        raise TypeError(
            f"Expected datetime.date or datetime.datetime for start, got {type(start)}"
        )
    if end is not None and not isinstance(end, (datetime.date, datetime.datetime)):
        raise TypeError(
            f"Expected datetime.date or datetime.datetime for end, got {type(end)}"
        )

    # validate step_days
    if step_days == 0:
        raise ValueError("step_days must not be 0")

    # convert start and end to date
    if isinstance(start, datetime.datetime):
        start = datetime_handler(start)
    if isinstance(end, datetime.datetime):
        end = datetime_handler(end)

    # set ascending and delta
    ASCENDING = step_days > 0
    DELTA = datetime.timedelta(days=step_days)

    # set start date and end date
    if not include_start:
        start += DELTA
    if ASCENDING and end is None:
        end = datetime.date.max
    elif not ASCENDING and end is None:
        end = datetime.date.min
    assert end is not None

    # set end date
    is_broken: Callable[[datetime.date], bool] = {
        (True, True): end.__lt__,
        (True, False): end.__le__,
        (False, True): end.__gt__,
        (False, False): end.__ge__,
    }[(ASCENDING, include_end)]

    # yield date
    for _ in count():
        if is_broken(start):
            break
        yield start
        try:
            start += DELTA
        except OverflowError:
            break
