import datetime
from typing import Callable

IsHolidayFuncType = Callable[[datetime.datetime | datetime.date], bool]  # noqa: E501


def is_saturday_or_sunday(
    date: datetime.datetime | datetime.date,
) -> bool:
    return date.weekday() in {5, 6}


def is_new_year_day(
    date: datetime.datetime | datetime.date,
) -> bool:
    return date.month == 1 and date.day == 1


def is_the_first_three_days_of_new_year(
    date: datetime.datetime | datetime.date,
) -> bool:
    return date.month == 1 and date.day <= 3


def is_the_end_of_year(
    date: datetime.datetime | datetime.date,
) -> bool:
    return date.month == 12 and date.day == 31


def is_between_1231_0103(
    date: datetime.datetime | datetime.date,
) -> bool:
    return is_the_end_of_year(date) or is_the_first_three_days_of_new_year(date)


class HolidayDiscriminator:

    def __init__(
        self,
        *funcs: IsHolidayFuncType,
        **kwargs: IsHolidayFuncType,
    ) -> None:
        self._is_holiday_funcs = {func.__name__: func for func in funcs}
        self._is_holiday_funcs.update(kwargs)

    def __call__(self, date: datetime.datetime | datetime.date) -> bool:
        return any(func(date) for func in self._is_holiday_funcs.values())

    @property
    def names(self) -> list[str]:
        return list(self._is_holiday_funcs.keys())

    @property
    def is_holiday_funcs(self) -> dict[str, IsHolidayFuncType]:
        return self._is_holiday_funcs.copy()

    def add_is_holiday_funcs(
        self,
        *is_holiday_funcs_args: IsHolidayFuncType,
        allow_overwrite: bool = False,
        **is_holiday_funcs_kwargs: IsHolidayFuncType,
    ) -> None:
        # preprocess
        dic: dict[str, IsHolidayFuncType] = {}
        for func in is_holiday_funcs_args:
            try:
                dic[func.__name__] = func
            except AttributeError as e:
                # TODO: more appropriate error handling
                raise e
        dic.update(is_holiday_funcs_kwargs)
        # check duplicates
        for name in dic.keys():
            if not allow_overwrite and name in self._is_holiday_funcs:
                raise ValueError(f"Function with name '{name}' already exists. Set allow_overwrite=True to overwrite.")  # noqa
        # add the new functions
        for name, is_holiday_func in dic.items():
            # TODO: more strict type checking
            self._is_holiday_funcs[name] = is_holiday_func

    def remove_is_holiday_funcs(
        self,
        *names: str,
    ) -> None:
        # check if names are in the dictionary
        for name in names:
            if name not in self._is_holiday_funcs:
                raise KeyError(f"Function with name '{name}' does not exist.")
        # remove the functions
        for name in names:
            self._is_holiday_funcs.pop(name)
