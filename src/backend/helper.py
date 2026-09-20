from datetime import date

from schema import DateRange


def is_already_booked(dates_booked: list[date], reservation_range: DateRange) -> bool:
    is_reserved = [
        day >= reservation_range.start_date and day <= reservation_range.end_date
        for day in dates_booked
    ]
    return any(is_reserved)
