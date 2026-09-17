from datetime import date, timedelta


def get_month_dates(year: int, month: int):
    first_day = date(year, month, 1)

    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)

    last_day = next_month - timedelta(days=1)
    return first_day, last_day


def is_service_day(day: date):
    return day.weekday() < 5


def get_service_days(start_date: date, end_date: date):
    days = []
    current = start_date

    while current <= end_date:
        if is_service_day(current):
            days.append(current)
        current += timedelta(days=1)

    return days
