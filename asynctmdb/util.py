from datetime import datetime

def date(dt):
    datetime.strptime(dt, "%Y-%m-%d").date()
