from app.utils.date_utils import get_service_days


def get_paused_service_days(service_days, pause_periods):
    paused = set()

    for pause in pause_periods:
        pause_days = get_service_days(pause.start_date, pause.end_date)
        for day in pause_days:
            if day in service_days:
                paused.add(day)

    return paused
