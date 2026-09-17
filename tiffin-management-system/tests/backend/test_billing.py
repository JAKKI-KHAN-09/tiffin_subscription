from datetime import date

from app.utils.date_utils import get_service_days


def test_weekday_calculation():
    days = get_service_days(date(2026, 9, 1), date(2026, 9, 30))
    assert all(day.weekday() < 5 for day in days)


def test_pause_reduces_served_days():
    scheduled_days = 22
    paused_days = 5
    served_days = scheduled_days - paused_days
    assert served_days == 17
