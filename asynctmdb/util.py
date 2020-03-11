from datetime import datetime

All = "All"


def date(dt):
    return datetime.strptime(dt, "%Y-%m-%d").date()
