import sys
import os
from win32api import SetSystemTime
from ntplib import NTPClient
from _datetime import datetime, timezone


def get_time(ntp_server: str = "time.windows.com") -> tuple:
    """
    Receives time stamp from given NTP server.

    :param str ntp_server: NTP server address.
    :return: Tuple of integers containing year, month, day, hour, minute, second, milisecond.
    :rtype: tuple
    """
    response = NTPClient().request(ntp_server, version=3)
    date = datetime.fromtimestamp(response.tx_time, timezone.utc)
    return (date.year, date.month, date.day,
            date.hour, date.minute, date.second,
            date.microsecond // 1000)


def set_time_zone_windows(time_zone: str = "Central European Standard Time") -> None:
    """
    Set given timezone in windows machine.
     * invokes tzutil Windows subroutine.

    :param str time_zone: Time zone given in windows standard.
    :return: Set specific time zone on the given windows machine.
    :rtype: None
    """
    os.system(f'tzutil /s "{time_zone}"')


def set_time_zone_linux(time_zone: str = 'Europe/Warsaw') -> None:
    """
    Set given timezone in linux standard.
     * invokes timedatectl Linux sub program.

    :param str time_zone: Time zone given in windows standard.
    :return: Set specific time zone on the given linux machine.
    :rtype: None
    """
    os.system(f"sudo timedatectl set-timezone {time_zone}")


def set_time_windows(time_tuple: tuple) -> None:
    """
    Set given time and date in Windows machine.
     * this script additionally sets workday on the machine.

    :param tuple time_tuple: time tuple containing year, month, day, hour, minute, second, milisecond.
    :return: Set time in Windows according to given tuple.
    :rtype: None
    """
    week_day = datetime(*time_tuple).isocalendar()[2]
    windows_time = time_tuple[:2] + (week_day,) + time_tuple[2:]
    SetSystemTime(*windows_time)


def set_time_linux(time_tuple: tuple) -> None:
    """
    Set given time and date in Linux machine.
     * this script additionally sets time in iso standard on the machine.
     * invokes timedatectl sub program and disables auto update time on machine.set_time
     * invokes date sub program and set's time.
     * invokes hwclock subprogram and set's time in the internal clock.

    :param tuple time_tuple: time tuple containing year, month, day, hour, minute, second, milisecond.
    :return: Set time in Linux according to given tuple.
    :rtype: None
    """
    linux_time = datetime(*time_tuple).isoformat()
    os.system(f"sudo timedatectl set-ntp false")
    os.system(f"sudo date -s {linux_time}")
    os.system(f"sudo hwclock -w")


def set_time() -> None:
    """
    Wrap's functions and run them accordingly to operating system they are run on.
     * in Windows machine run's: set_time_windows, set time windows.
     * in Linux machine run's: set_time_linux, set_time_zone_linux.

    :return: Run given functions of this script.
    :rtype: None
    """
    if sys.platform == "win32":
        set_time_windows(time_tuple=get_time())
        set_time_zone_windows()
    if sys.platform == "linux":
        set_time_linux(time_tuple=get_time())
        set_time_zone_linux()


if __name__ == "__main__":
    set_time()
