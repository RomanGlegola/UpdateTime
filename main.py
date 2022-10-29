import sys
import os
from win32api import SetSystemTime
from ntplib import NTPClient
from _datetime import datetime, timezone


def get_time() -> tuple:
    ntp_server: str = "time.windows.com"
    response = NTPClient().request(ntp_server, version=3)
    date = datetime.fromtimestamp(response.tx_time, timezone.utc)
    return (date.year, date.month, date.day,
            date.hour, date.minute, date.second,
            date.microsecond // 1000)


def set_time_zone_windows() -> None:
    time_zone: str = "Central European Standard Time"
    os.system(f'tzutil /s "{time_zone}"')


def set_time_zone_linux() -> None:
    time_zone: str = 'Europe/Warsaw'
    os.system(f"sudo timedatectl set-timezone {time_zone}")


def set_time_windows(time_tuple: tuple) -> None:
    week_day = datetime(*time_tuple).isocalendar()[2]
    windows_time = time_tuple[:2] + (week_day,) + time_tuple[2:]
    SetSystemTime(*windows_time)


def set_time_linux(time_tuple: tuple) -> None:
    linux_time = datetime(*time_tuple).isoformat()
    os.system(f"sudo timedatectl set-ntp false")
    os.system(f"sudo date -s {linux_time}")
    os.system(f"sudo hwclock -w")


def set_time() -> None:
    if sys.platform == "win32":
        set_time_windows(time_tuple=get_time())
        set_time_zone_windows()
    if sys.platform == "linux":
        set_time_linux(time_tuple=get_time())
        set_time_zone_linux()


if __name__ == "__main__":
    set_time()
