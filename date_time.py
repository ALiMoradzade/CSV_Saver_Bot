import datetime
import pytz
from persiantools.jdatetime import JalaliDate

# Install persiantools


def tehran_datetime(string_format: str) -> str:
    time_zone = pytz.timezone("Asia/Tehran")
    time_zone_formatted = datetime.datetime.now(time_zone).strftime(string_format)
    return time_zone_formatted


def persian_date(string_format: str) -> str:
    return JalaliDate(datetime.date.today()).strftime(string_format)
