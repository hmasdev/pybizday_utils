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
    if is_holiday(date):
        return False
    return date.month != (get_next_bizday(date, is_holiday)).month


def is_biz_start_of_month(
    date: datetime.date,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
) -> bool:
    if is_holiday(date):
        return False
    return date.month != (get_prev_bizday(date, is_holiday)).month


def get_biz_end_of_month(
    date: datetime.date,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
) -> datetime.date:
    date = date.replace(day=1)  # start of month
    date = date + datetime.timedelta(days=31)
    date = date.replace(day=1)  # start of next month
    return get_prev_bizday(date, is_holiday)


def get_biz_start_of_month(
    date: datetime.date,
    is_holiday: IsHolidayFuncType = global_default_holiday_discriminator,
) -> datetime.date:
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
    return add_years_months(
        date,
        0,
        months,
        is_holiday,
        bizeom2bizeom=bizeom2bizeom,
        bizsom2bizsom=bizsom2bizsom,
    )
