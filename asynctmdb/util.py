from datetime import datetime

All = "All"

def date(dt):
    datetime.strptime(dt, "%Y-%m-%d").date()
