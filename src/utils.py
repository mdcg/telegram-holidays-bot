from datetime import datetime
from src import logger
from src.exceptions import NoNextHolidaysException
from src.constants import WEEKENDS
from src.readers import read_csv


def next_holiday(csv_path):
    logger.info("Looking for next holiday...")

    vacations = read_csv(csv_path)
    now = datetime.now()

    for v in vacations:
        vacation_date = datetime.strptime(v["date"], "%d/%m/%Y")
        if vacation_date >= now:
            return v

    raise NoNextHolidaysException()


def how_many_days_until_the_holiday(_date):
    logger.info("Calculating how many days are left until the next holiday...")

    now = datetime.now()
    vacation_date = datetime.strptime(_date, "%d/%m/%Y")
    delta = vacation_date - now
    days_until_holiday = delta.days

    logger.info(f"{days_until_holiday} days until the next holiday...")
    return days_until_holiday


def today_is_a_holiday(days_until_the_holiday):
    is_today = days_until_the_holiday == 0
    logger.info(f"Is today a holiday? {is_today}")

    return is_today


def generate_message_by_date(holiday_info, country_info):
    logger.info("Generating bot message for the next holiday...")

    days_until_the_holiday = how_many_days_until_the_holiday(holiday_info["date"])
    if today_is_a_holiday(days_until_the_holiday):
        return country_info["TODAY_IS_HOLIDAY_MESSAGE"].format(holiday_info["holiday_name"])

    days_until_the_holiday_message = country_info["NEXT_HOLIDAY_MESSAGE"].format(
        days_until_the_holiday
    )

    if holiday_info["weekday_name"].lower() in WEEKENDS:
        base_message = country_info["WEEKEND_MESSAGE"].format(holiday_info["weekday_name"])
    else:
        base_message = country_info["WEEKDAY_MESSAGE"].format(holiday_info["weekday_name"])

    holiday_name_message = country_info["HOLIDAY_NAME_MESSAGE"].format(holiday_info["holiday_name"])

    logger.info("Sending message...")
    return f"{base_message}{days_until_the_holiday_message}{holiday_name_message}"
