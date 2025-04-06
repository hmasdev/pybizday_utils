import datetime
from typing import Callable

import pytest

from pybizday_utils.basic import (
    bizday_range,
    count_bizdays,
    get_n_next_bizday,
    get_n_prev_bizday,
    get_next_bizday,
    get_prev_bizday,
    is_bizday,
)


@pytest.mark.positive
@pytest.mark.parametrize(
    "date, is_holiday, expected",
    [
        (datetime.date(2021, 1, 1), lambda d: d == datetime.date(2021, 1, 1), False),  # noqa
        (datetime.date(2021, 1, 2), lambda d: d == datetime.date(2021, 1, 3), True),  # noqa
    ],
)
def test_is_bizday(
    date: datetime.date,
    is_holiday: Callable[[datetime.date], bool],
    expected: bool,
) -> None:
    assert is_bizday(date, is_holiday) == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "date, is_holiday, expected",
    [
        (
            datetime.date(2025, 4, 25),
            lambda _: False,
            datetime.date(2025, 4, 26),
        ),
        (
            datetime.date(2025, 4, 25),
            lambda d: d == (datetime.date(2025, 4, 26)),
            datetime.date(2025, 4, 27),
        ),
        (
            datetime.date(2025, 4, 25),
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27)},  # noqa
            datetime.date(2025, 4, 28),
        ),
    ],
)
def test_get_next_bizday(
    date: datetime.date,
    is_holiday: Callable[[datetime.date], bool],
    expected: datetime.date,
) -> None:
    assert get_next_bizday(date, is_holiday) == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "date, is_holiday, expected",
    [
        (
            datetime.date(2025, 4, 25),
            lambda _: False,
            datetime.date(2025, 4, 24),
        ),
        (
            datetime.date(2025, 4, 25),
            lambda d: d == (datetime.date(2025, 4, 24)),
            datetime.date(2025, 4, 23),
        ),
        (
            datetime.date(2025, 4, 25),
            lambda d: d in {datetime.date(2025, 4, 24), datetime.date(2025, 4, 23)},  # noqa
            datetime.date(2025, 4, 22),
        ),
    ],
)
def test_get_prev_bizday(
    date: datetime.date,
    is_holiday: Callable[[datetime.date], bool],
    expected: datetime.date,
) -> None:
    assert get_prev_bizday(date, is_holiday) == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "date, n, is_holiday, expected",
    [
        (
            datetime.date(2025, 4, 25),
            1,
            lambda _: False,
            datetime.date(2025, 4, 26),
        ),
        (
            datetime.date(2025, 4, 25),
            1,
            lambda d: d == (datetime.date(2025, 4, 26)),
            datetime.date(2025, 4, 27),
        ),
        (
            datetime.date(2025, 4, 25),
            1,
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27)},  # noqa
            datetime.date(2025, 4, 28),
        ),
        (
            datetime.date(2025, 4, 25),
            -1,
            lambda _: False,
            datetime.date(2025, 4, 24),
        ),
        (
            datetime.date(2025, 4, 25),
            -1,
            lambda d: d == (datetime.date(2025, 4, 24)),
            datetime.date(2025, 4, 23),
        ),
        (
            datetime.date(2025, 4, 25),
            -1,
            lambda d: d in {datetime.date(2025, 4, 24), datetime.date(2025, 4, 23)},  # noqa
            datetime.date(2025, 4, 22),
        ),
        (
            datetime.date(2025, 4, 25),
            0,
            lambda _: False,
            datetime.date(2025, 4, 25),
        ),
        (
            datetime.date(2025, 4, 25),
            2,
            lambda _: False,
            datetime.date(2025, 4, 27),
        ),
        (
            datetime.date(2025, 4, 25),
            2,
            lambda d: d == (datetime.date(2025, 4, 26)),
            datetime.date(2025, 4, 28),
        ),
        (
            datetime.date(2025, 4, 25),
            2,
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27)},  # noqa
            datetime.date(2025, 4, 29),
        ),
        (
            datetime.date(2025, 4, 25),
            2,
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27), datetime.date(2025, 4, 29)},  # noqa
            datetime.date(2025, 4, 30),
        ),
        (
            datetime.date(2025, 4, 27),
            -2,
            lambda _: False,
            datetime.date(2025, 4, 25),
        ),
        (
            datetime.date(2025, 4, 28),
            -2,
            lambda d: d == (datetime.date(2025, 4, 26)),
            datetime.date(2025, 4, 25),
        ),
        (
            datetime.date(2025, 4, 29),
            -2,
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27)},  # noqa
            datetime.date(2025, 4, 25),
        ),
        (
            datetime.date(2025, 4, 30),
            -2,
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27), datetime.date(2025, 4, 29)},  # noqa
            datetime.date(2025, 4, 25),
        ),
    ],
)
def test_get_n_next_bizday(
    date: datetime.date,
    n: int,
    is_holiday: Callable[[datetime.date], bool],
    expected: datetime.date,
) -> None:
    assert get_n_next_bizday(date, n, is_holiday) == expected


@pytest.mark.negative
def test_get_n_next_bizday_with_n_0_and_date_holiday() -> None:
    date = datetime.date(2025, 4, 25)
    def is_holiday(d: datetime.date) -> bool: return True
    with pytest.raises(ValueError):
        get_n_next_bizday(date, 0, is_holiday)


@pytest.mark.positive
@pytest.mark.parametrize(
    "date, n, is_holiday, expected",
    [
        (
            datetime.date(2025, 4, 25),
            -1,
            lambda _: False,
            datetime.date(2025, 4, 26),
        ),
        (
            datetime.date(2025, 4, 25),
            -1,
            lambda d: d == (datetime.date(2025, 4, 26)),
            datetime.date(2025, 4, 27),
        ),
        (
            datetime.date(2025, 4, 25),
            -1,
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27)},  # noqa
            datetime.date(2025, 4, 28),
        ),
        (
            datetime.date(2025, 4, 25),
            1,
            lambda _: False,
            datetime.date(2025, 4, 24),
        ),
        (
            datetime.date(2025, 4, 25),
            1,
            lambda d: d == (datetime.date(2025, 4, 24)),
            datetime.date(2025, 4, 23),
        ),
        (
            datetime.date(2025, 4, 25),
            1,
            lambda d: d in {datetime.date(2025, 4, 24), datetime.date(2025, 4, 23)},  # noqa
            datetime.date(2025, 4, 22),
        ),
        (
            datetime.date(2025, 4, 25),
            0,
            lambda _: False,
            datetime.date(2025, 4, 25),
        ),
        (
            datetime.date(2025, 4, 25),
            -2,
            lambda _: False,
            datetime.date(2025, 4, 27),
        ),
        (
            datetime.date(2025, 4, 25),
            -2,
            lambda d: d == (datetime.date(2025, 4, 26)),
            datetime.date(2025, 4, 28),
        ),
        (
            datetime.date(2025, 4, 25),
            -2,
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27)},  # noqa
            datetime.date(2025, 4, 29),
        ),
        (
            datetime.date(2025, 4, 25),
            -2,
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27), datetime.date(2025, 4, 29)},  # noqa
            datetime.date(2025, 4, 30),
        ),
        (
            datetime.date(2025, 4, 27),
            2,
            lambda _: False,
            datetime.date(2025, 4, 25),
        ),
        (
            datetime.date(2025, 4, 28),
            2,
            lambda d: d == (datetime.date(2025, 4, 26)),
            datetime.date(2025, 4, 25),
        ),
        (
            datetime.date(2025, 4, 29),
            2,
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27)},  # noqa
            datetime.date(2025, 4, 25),
        ),
        (
            datetime.date(2025, 4, 30),
            2,
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27), datetime.date(2025, 4, 29)},  # noqa
            datetime.date(2025, 4, 25),
        ),
    ],
)
def test_get_n_prev_bizday(
    date: datetime.date,
    n: int,
    is_holiday: Callable[[datetime.date], bool],
    expected: datetime.date,
) -> None:
    assert get_n_prev_bizday(date, n, is_holiday) == expected


@pytest.mark.negative
def test_get_n_prev_bizday_with_n_0_and_date_holiday() -> None:
    date = datetime.date(2025, 4, 25)
    def is_holiday(d: datetime.date) -> bool: return True
    with pytest.raises(ValueError):
        get_n_prev_bizday(date, 0, is_holiday)


@pytest.mark.positive
@pytest.mark.parametrize(
    "start, end, is_holiday, include_start, include_end, expected",
    [
        (
            datetime.date(2025, 4, 25),
            datetime.date(2025, 4, 30),
            lambda _: False,
            True,
            True,
            [
                datetime.date(2025, 4, 25),
                datetime.date(2025, 4, 26),
                datetime.date(2025, 4, 27),
                datetime.date(2025, 4, 28),
                datetime.date(2025, 4, 29),
                datetime.date(2025, 4, 30),
            ],
        ),
        (
            datetime.date(2025, 4, 25),
            datetime.date(2025, 4, 30),
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27), datetime.date(2025, 4, 29)},  # noqa
            True,
            True,
            [
                datetime.date(2025, 4, 25),
                datetime.date(2025, 4, 28),
                datetime.date(2025, 4, 30),
            ],
        ),
        (
            datetime.date(2025, 4, 25),
            datetime.date(2025, 4, 30),
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27), datetime.date(2025, 4, 29)},  # noqa
            False,
            True,
            [
                datetime.date(2025, 4, 28),
                datetime.date(2025, 4, 30),
            ],
        ),
        (
            datetime.date(2025, 4, 25),
            datetime.date(2025, 4, 30),
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27), datetime.date(2025, 4, 29)},  # noqa
            True,
            False,
            [
                datetime.date(2025, 4, 25),
                datetime.date(2025, 4, 28),
            ],
        ),
        (
            datetime.date(2025, 4, 25),
            datetime.date(2025, 4, 30),
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27), datetime.date(2025, 4, 29)},  # noqa
            False,
            False,
            [
                datetime.date(2025, 4, 28),
            ],
        ),
        (
            datetime.date(2025, 4, 30),
            datetime.date(2025, 4, 25),
            lambda _: False,
            True,
            True,
            [
                datetime.date(2025, 4, 30),
                datetime.date(2025, 4, 29),
                datetime.date(2025, 4, 28),
                datetime.date(2025, 4, 27),
                datetime.date(2025, 4, 26),
                datetime.date(2025, 4, 25),
            ],
        ),
        (
            datetime.date(2025, 4, 30),
            datetime.date(2025, 4, 25),
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27), datetime.date(2025, 4, 29)},  # noqa
            True,
            True,
            [
                datetime.date(2025, 4, 30),
                datetime.date(2025, 4, 28),
                datetime.date(2025, 4, 25),
            ],
        ),
        (
            datetime.date(2025, 4, 30),
            datetime.date(2025, 4, 25),
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27), datetime.date(2025, 4, 29)},  # noqa
            False,
            True,
            [
                datetime.date(2025, 4, 28),
                datetime.date(2025, 4, 25),
            ],
        ),
        (
            datetime.date(2025, 4, 30),
            datetime.date(2025, 4, 25),
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27), datetime.date(2025, 4, 29)},  # noqa
            True,
            False,
            [
                datetime.date(2025, 4, 30),
                datetime.date(2025, 4, 28),
            ],
        ),
        (
            datetime.date(2025, 4, 30),
            datetime.date(2025, 4, 25),
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27), datetime.date(2025, 4, 29)},  # noqa
            False,
            False,
            [
                datetime.date(2025, 4, 28),
            ],
        )
    ],
)
def test_bizday_range(
    start: datetime.date,
    end: datetime.date,
    is_holiday: Callable[[datetime.date], bool],
    include_start: bool,
    include_end: bool,
    expected: list[datetime.date],
) -> None:
    actual = list(bizday_range(
        start,
        end,
        is_holiday,
        include_start=include_start,
        include_end=include_end,
    ))
    assert actual == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "start, end, is_holiday, include_start, include_end, expected",
    [
        (
            datetime.date(2025, 4, 25),
            datetime.date(2025, 4, 30),
            lambda _: False,
            True,
            True,
            6,
        ),
        (
            datetime.date(2025, 4, 25),
            datetime.date(2025, 4, 30),
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27), datetime.date(2025, 4, 29)},  # noqa
            True,
            True,
            3,
        ),
        (
            datetime.date(2025, 4, 25),
            datetime.date(2025, 4, 30),
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27), datetime.date(2025, 4, 29)},  # noqa
            False,
            True,
            2,
        ),
        (
            datetime.date(2025, 4, 25),
            datetime.date(2025, 4, 30),
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27), datetime.date(2025, 4, 29)},  # noqa
            True,
            False,
            2,
        ),
        (
            datetime.date(2025, 4, 25),
            datetime.date(2025, 4, 30),
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27), datetime.date(2025, 4, 29)},  # noqa
            False,
            False,
            1,
        ),
        (
            datetime.date(2025, 4, 30),
            datetime.date(2025, 4, 25),
            lambda _: False,
            True,
            True,
            -6,
        ),
        (
            datetime.date(2025, 4, 30),
            datetime.date(2025, 4, 25),
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27), datetime.date(2025, 4, 29)},  # noqa
            True,
            True,
            -3,
        ),
        (
            datetime.date(2025, 4, 30),
            datetime.date(2025, 4, 25),
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27), datetime.date(2025, 4, 29)},  # noqa
            False,
            True,
            -2,
        ),
        (
            datetime.date(2025, 4, 30),
            datetime.date(2025, 4, 25),
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27), datetime.date(2025, 4, 29)},  # noqa
            True,
            False,
            -2,
        ),
        (
            datetime.date(2025, 4, 30),
            datetime.date(2025, 4, 25),
            lambda d: d in {datetime.date(2025, 4, 26), datetime.date(2025, 4, 27), datetime.date(2025, 4, 29)},  # noqa
            False,
            False,
            -1,
        )
    ],
)
def test_count_bizdays(
    start: datetime.date,
    end: datetime.date,
    is_holiday: Callable[[datetime.date], bool],
    include_start: bool,
    include_end: bool,
    expected: int,
) -> None:
    actual = count_bizdays(
        start,
        end,
        is_holiday,
        include_start=include_start,
        include_end=include_end,
    )
    assert actual == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    'd, handler, is_holiday',
    [
        (
            datetime.datetime(2021, 1, 1),
            lambda dt: dt.date(),
            lambda d: d == datetime.date(2021, 1, 1),
        ),
        (
            datetime.datetime(2021, 1, 2),
            lambda dt: dt.date(),
            lambda d: d == datetime.date(2021, 1, 3),
        ),
        (
            datetime.datetime(2021, 1, 3),
            lambda _: datetime.date(2024, 1, 1),
            lambda d: d == datetime.date(2024, 1, 1),
        ),
    ],
)
def test_is_bizday_with_datetime_obj_should_return_the_same_result_of_is_bizyday_with_handled_obj(  # noqa: E501
    d: datetime.datetime,
    handler: Callable[[datetime.datetime], datetime.date],
    is_holiday: Callable[[datetime.date], bool],
) -> None:
    handled_d = handler(d)
    assert is_bizday(d, is_holiday, datetime_handler=handler) == is_bizday(handled_d, is_holiday)  # noqa: E501


@pytest.mark.positive
@pytest.mark.parametrize(
    'd, handler, is_holiday',
    [
        (
            datetime.datetime(2021, 1, 1),
            lambda dt: dt.date(),
            lambda d: d == datetime.date(2021, 1, 1),
        ),
        (
            datetime.datetime(2021, 1, 2),
            lambda dt: dt.date(),
            lambda d: d == datetime.date(2021, 1, 3),
        ),
        (
            datetime.datetime(2021, 1, 3),
            lambda _: datetime.date(2024, 1, 3),
            lambda d: d == datetime.date(2024, 1, 4),
        ),
    ],
)
def test_get_next_bizday_with_datetime_obj_should_return_the_same_result_of_get_next_bizday_with_handled_obj(  # noqa: E501
    d: datetime.datetime,
    handler: Callable[[datetime.datetime], datetime.date],
    is_holiday: Callable[[datetime.date], bool],
) -> None:
    handled_d = handler(d)
    assert get_next_bizday(d, is_holiday, datetime_handler=handler) == get_next_bizday(handled_d, is_holiday)  # noqa: E501


@pytest.mark.positive
@pytest.mark.parametrize(
    'd, handler, is_holiday',
    [
        (
            datetime.datetime(2021, 1, 1),
            lambda dt: dt.date(),
            lambda d: d == datetime.date(2021, 1, 1),
        ),
        (
            datetime.datetime(2021, 1, 2),
            lambda dt: dt.date(),
            lambda d: d == datetime.date(2021, 1, 3),
        ),
        (
            datetime.datetime(2021, 1, 3),
            lambda _: datetime.date(2024, 1, 3),
            lambda d: d == datetime.date(2024, 1, 2),
        ),
    ],
)
def test_get_prev_bizday_with_datetime_obj_should_return_the_same_result_of_get_prev_bizday_with_handled_obj(  # noqa: E501
    d: datetime.datetime,
    handler: Callable[[datetime.datetime], datetime.date],
    is_holiday: Callable[[datetime.date], bool],
) -> None:
    handled_d = handler(d)
    assert get_prev_bizday(d, is_holiday, datetime_handler=handler) == get_prev_bizday(handled_d, is_holiday)  # noqa: E501


@pytest.mark.positive
@pytest.mark.parametrize(
    'd, handler, n, is_holiday',
    [
        (
            datetime.datetime(2021, 1, 1),
            lambda dt: dt.date(),
            1,
            lambda d: d == datetime.date(2021, 1, 1),
        ),
        (
            datetime.datetime(2021, 1, 2),
            lambda dt: dt.date(),
            -1,
            lambda d: d == datetime.date(2021, 1, 3),
        ),
        (
            datetime.datetime(2021, 1, 3),
            lambda _: datetime.date(2024, 1, 3),
            2,
            lambda d: d == datetime.date(2024, 1, 4),
        ),
    ],
)
def test_get_n_next_bizday_with_datetime_obj_should_return_the_same_result_of_get_n_next_bizday_with_handled_obj(  # noqa: E501
    d: datetime.datetime,
    handler: Callable[[datetime.datetime], datetime.date],
    n: int,
    is_holiday: Callable[[datetime.date], bool],
) -> None:
    handled_d = handler(d)
    assert get_n_next_bizday(d, n, is_holiday, datetime_handler=handler) == get_n_next_bizday(handled_d, n, is_holiday)  # noqa: E501


@pytest.mark.positive
@pytest.mark.parametrize(
    'd, handler, n, is_holiday',
    [
        (
            datetime.datetime(2021, 1, 1),
            lambda dt: dt.date(),
            -1,
            lambda d: d == datetime.date(2021, 1, 1),
        ),
        (
            datetime.datetime(2021, 1, 2),
            lambda dt: dt.date(),
            1,
            lambda d: d == datetime.date(2021, 1, 3),
        ),
        (
            datetime.datetime(2021, 1, 3),
            lambda _: datetime.date(2024, 1, 3),
            2,
            lambda d: d == datetime.date(2024, 1, 2),
        ),
    ],
)
def test_get_n_prev_bizday_with_datetime_obj_should_return_the_same_result_of_get_n_prev_bizday_with_handled_obj(  # noqa: E501
    d: datetime.datetime,
    handler: Callable[[datetime.datetime], datetime.date],
    n: int,
    is_holiday: Callable[[datetime.date], bool],
) -> None:
    handled_d = handler(d)
    assert get_n_prev_bizday(d, n, is_holiday, datetime_handler=handler) == get_n_prev_bizday(handled_d, n, is_holiday)  # noqa: E501


@pytest.mark.positive
@pytest.mark.parametrize(
    'start, end, handler, is_holiday',
    [
        (
            datetime.datetime(2021, 1, 1),
            datetime.datetime(2021, 1, 10),
            lambda dt: dt.date(),
            lambda d: d == datetime.date(2021, 1, 3),
        ),
        (
            datetime.datetime(2021, 1, 2),
            datetime.datetime(2021, 1, 11),
            lambda dt: dt.date(),
            lambda d: d == datetime.date(2021, 1, 3),
        ),
        (
            datetime.datetime(2021, 1, 3),
            datetime.datetime(2021, 1, 12),
            lambda dt: (dt + datetime.timedelta(days=10)).date(),
            lambda d: d == datetime.date(2024, 1, 15),
        ),
    ],
)
def test_bizday_range_with_datetime_obj_should_return_the_same_result_of_bizday_range_with_handled_obj(  # noqa: E501
    start: datetime.datetime,
    end: datetime.datetime,
    handler: Callable[[datetime.datetime], datetime.date],
    is_holiday: Callable[[datetime.date], bool],
) -> None:
    handled_start = handler(start)
    handled_end = handler(end)
    assert list(bizday_range(
        start,
        end,
        is_holiday,
        datetime_handler=handler,
    )) == list(bizday_range(handled_start, handled_end, is_holiday))  # noqa: E501


@pytest.mark.positive
@pytest.mark.parametrize(
    'start, end, handler, is_holiday',
    [
        (
            datetime.datetime(2021, 1, 1),
            datetime.datetime(2021, 1, 10),
            lambda dt: dt.date(),
            lambda d: d == datetime.date(2021, 1, 1),
        ),
        (
            datetime.datetime(2021, 1, 2),
            datetime.datetime(2021, 1, 11),
            lambda dt: dt.date(),
            lambda d: d == datetime.date(2021, 1, 3),
        ),
        (
            datetime.datetime(2021, 1, 3),
            datetime.datetime(2021, 1, 12),
            lambda dt: (dt + datetime.timedelta(days=10)).date(),
            lambda d: d == datetime.date(2024, 1, 15),
        ),
    ],
)
def test_count_bizdays_with_datetime_obj_should_return_the_same_result_of_count_bizdays_with_handled_obj(  # noqa: E501
    start: datetime.datetime,
    end: datetime.datetime,
    handler: Callable[[datetime.datetime], datetime.date],
    is_holiday: Callable[[datetime.date], bool],
) -> None:
    handled_start = handler(start)
    handled_end = handler(end)
    assert count_bizdays(
        start,
        end,
        is_holiday,
        datetime_handler=handler,
    ) == count_bizdays(handled_start, handled_end, is_holiday)
