import datetime

from dateutil.relativedelta import relativedelta

from .basic import (
    get_next_bizday,
    get_prev_bizday,
)
from .default_holiday_utils import global_default_holiday_discriminator
from .holiday_utils import IsHolidayFuncType


def is_biz_end_of_month(
    date: datetime.date,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
) -> bool:
    """Check if the given date is the last business day of the month.

    Args:
        date (datetime.date): Date to check.
        is_holiday (IsHolidayFuncType, optional): Function to check if a date is a holiday.
            Defaults to global_default_holiday_discriminator.

    Returns:
        bool: True if the date is the last business day of the month, False otherwise.
    """  # noqa: E501
    if is_holiday(date):
        return False
    return date.month != (get_next_bizday(date, is_holiday)).month


def is_biz_start_of_month(
    date: datetime.date,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
) -> bool:
    """Check if the given date is the first business day of the month.

    Args:
        date (datetime.date): Date to check.
        is_holiday (IsHolidayFuncType, optional): Function to check if a date is a holiday.
            Defaults to global_default_holiday_discriminator.

    Returns:
        bool: True if the date is the first business day of the month, False otherwise.
    """  # noqa: E501
    if is_holiday(date):
        return False
    return date.month != (get_prev_bizday(date, is_holiday)).month


def get_biz_end_of_month(
    date: datetime.date,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
) -> datetime.date:
    """Get the last business day of the month for the given date.

    Args:
        date (datetime.date): reference date.
        is_holiday (IsHolidayFuncType, optional): function to check if a date is a holiday.
            Defaults to global_default_holiday_discriminator.

    Returns:
        datetime.date: last business day of the month for the given date.
    """  # noqa: E501
    date = date.replace(day=1)  # start of month
    date = date + datetime.timedelta(days=31)
    date = date.replace(day=1)  # start of next month
    return get_prev_bizday(date, is_holiday)


def get_biz_start_of_month(
    date: datetime.date,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
) -> datetime.date:
    """Get the first business day of the month for the given date.

    Args:
        date (datetime.date): reference date.
        is_holiday (IsHolidayFuncType, optional): function to check if a date is a holiday.
            Defaults to global_default_holiday_discriminator.

    Returns:
        datetime.date: first business day of the month for the given date.
    """  # noqa: E501
    date = date.replace(day=1)  # start of month
    date = date - datetime.timedelta(days=1)  # end of previous month
    return get_next_bizday(date, is_holiday)


def add_years_months(
    date: datetime.date,
    years: int,
    months: int,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
    *,
    bizeom2bizeom: bool = True,
    bizsom2bizsom: bool = False,
) -> datetime.date:
    """Add years and months to a date with business day adjustment.

    Args:
        date (datetime.date): Reference date.
        years (int): Years to add
        months (int): Months to add
        is_holiday (IsHolidayFuncType, optional): function to check if a date is a holiday.
            Defaults to global_default_holiday_discriminator.
        bizeom2bizeom (bool, optional): Whether to adjust to the last business day of the month
            if the date is the last business day of the month. Defaults to True.
        bizsom2bizsom (bool, optional): Whether to adjust to the first business day of the month
            if the date is the first business day of the month. Defaults to False.

    Returns:
        datetime.date: Date after adding years and months with business day adjustment.
    """  # noqa: E501
    added = date + relativedelta(years=years, months=months)
    if bizeom2bizeom and is_biz_end_of_month(date, is_holiday):
        return get_biz_end_of_month(added, is_holiday)
    elif bizsom2bizsom and is_biz_start_of_month(date, is_holiday):
        return get_biz_start_of_month(added, is_holiday)
    else:
        return added


def add_years(
    date: datetime.date,
    years: int,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
    *,
    bizeom2bizeom: bool = True,
    bizsom2bizsom: bool = False,
) -> datetime.date:
    """Add years to a date with business day adjustment.
    This function is a wrapper around add_years_months with months set to 0.

    Args:
        date (datetime.date): Reference date.
        years (int): Years to add
        is_holiday (IsHolidayFuncType, optional): function to check if a date is a holiday.
            Defaults to global_default_holiday_discriminator.
        bizeom2bizeom (bool, optional): Whether to adjust to the last business day of the month
            if the date is the last business day of the month. Defaults to True.
        bizsom2bizsom (bool, optional): Whether to adjust to the first business day of the month
            if the date is the first business day of the month. Defaults to False.

    Returns:
        datetime.date: Date after adding years with business day adjustment.
    """  # noqa: E501
    return add_years_months(
        date,
        years,
        0,
        is_holiday,
        bizeom2bizeom=bizeom2bizeom,
        bizsom2bizsom=bizsom2bizsom,
    )


def add_months(
    date: datetime.date,
    months: int,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
    *,
    bizeom2bizeom: bool = True,
    bizsom2bizsom: bool = False,
) -> datetime.date:
    """Add months to a date with business day adjustment.
    This function is a wrapper around add_years_months with years set to 0.

    Args:
        date (datetime.date): Reference date.
        months (int): Months to add
        is_holiday (IsHolidayFuncType, optional): function to check if a date is a holiday.
            Defaults to global_default_holiday_discriminator.
        bizeom2bizeom (bool, optional): Whether to adjust to the last business day of the month
            if the date is the last business day of the month. Defaults to True.
        bizsom2bizsom (bool, optional): Whether to adjust to the first business day of the month
            if the date is the first business day of the month. Defaults to False.

    Returns:
        datetime.date: Date after adding months with business day adjustment.
    """  # noqa: E501
    return add_years_months(
        date,
        0,
        months,
        is_holiday,
        bizeom2bizeom=bizeom2bizeom,
        bizsom2bizsom=bizsom2bizsom,
    )
