from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from .holiday_utils import (
    HolidayDiscriminator,
    IsHolidayFuncType,
    is_saturday_or_sunday,
)


class _GlobalDefaultHolidayDiscriminator(HolidayDiscriminator):

    _instance: _GlobalDefaultHolidayDiscriminator | None = None

    def __new__(cls, *args, **kwargs) -> _GlobalDefaultHolidayDiscriminator:  # type: ignore
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def get_instance(cls) -> _GlobalDefaultHolidayDiscriminator:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


def add_global_is_holiday_funcs(
    *is_holiday_funcs_args: IsHolidayFuncType,
    allow_overwrite: bool = False,
    **is_holiday_funcs_kwargs: IsHolidayFuncType,
) -> None:
    default = _GlobalDefaultHolidayDiscriminator.get_instance()
    default.add_is_holiday_funcs(
        *is_holiday_funcs_args,
        allow_overwrite=allow_overwrite,
        **is_holiday_funcs_kwargs,
    )


def remove_global_is_holiday_funcs(
    *names: str,
) -> None:
    default = _GlobalDefaultHolidayDiscriminator.get_instance()
    default.remove_is_holiday_funcs(*names)


def get_global_holiday_funcs_names() -> list[str]:
    default = _GlobalDefaultHolidayDiscriminator.get_instance()
    return default.names


def get_global_holiday_funcs() -> dict[str, IsHolidayFuncType]:
    default = _GlobalDefaultHolidayDiscriminator.get_instance()
    return default.is_holiday_funcs


@contextmanager
def with_is_holiday_funcs(
    *is_holiday_funcs_args: IsHolidayFuncType,
    allow_overwrite: bool = False,
    all_replace: bool = False,
    **is_holiday_funcs_kwargs: IsHolidayFuncType,
) -> Generator[HolidayDiscriminator, None, None]:

    # Get the default holiday discriminator instance
    default = _GlobalDefaultHolidayDiscriminator.get_instance()
    # Cache the current holiday functions
    _cache = default.is_holiday_funcs

    # If all_replace is True, remove all current holiday functions
    if all_replace:
        default.remove_is_holiday_funcs(*default.names)

    # add the new holiday functions
    default.add_is_holiday_funcs(
        *is_holiday_funcs_args,
        allow_overwrite=allow_overwrite,
        **is_holiday_funcs_kwargs,
    )

    try:
        yield default
    finally:
        # remove all holiday functions
        default.remove_is_holiday_funcs(*default.names)
        # Restore the original state
        default.add_is_holiday_funcs(**_cache, allow_overwrite=True)


# initialize the default holiday functions
global_default_holiday_discriminator = _GlobalDefaultHolidayDiscriminator.get_instance()  # noqa: E501
global_default_holiday_discriminator.add_is_holiday_funcs(
    is_saturday_or_sunday,
    allow_overwrite=True,
)
