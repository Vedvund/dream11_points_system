import time
from datetime import datetime, timedelta, timezone


def has_time_passed(target_time="08:59:59"):
    now = datetime.now()
    today_target = datetime.strptime(target_time, "%H:%M:%S").replace(
        year=now.year, month=now.month, day=now.day
    )
    return now > today_target


def wait_until_target_time(target_time="08:59:59"):
    if has_time_passed(target_time):
        return
    now = datetime.now()
    today_target = datetime.strptime(target_time, "%H:%M:%S").replace(
        year=now.year, month=now.month, day=now.day
    )
    if today_target <= now:
        today_target += timedelta(days=1)
    time_diff = (today_target - now).total_seconds()
    time.sleep(time_diff)


def get_curr_time_ist():
    offset = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(offset)
