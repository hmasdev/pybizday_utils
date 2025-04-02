import datetime
from itertools import count
from typing import Callable, Generator


def date_range(
    start: datetime.date,
    end: datetime.date | None = None,
    *,
    include_start: bool = True,
    include_end: bool = True,
    step_days: int = 1,
) -> Generator[datetime.date, None, None]:
    """date generator from start to end.

    Args:
        start (datetime.date): start date
        end (datetime.date | None, optional): end date. Defaults to None.
        include_start (bool, optional): include start date. Defaults to True.
        include_end (bool, optional): include end date. Defaults to True.
        step_days (int, optional): step days. Defaults to 1

    Yields:
        Generator[datetime.date, None, None]: date generator

    Raises:
        ValueError: step_days is 0
    """
    # validate step_days
    if step_days == 0:
        raise ValueError("step_days must not be 0")

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
