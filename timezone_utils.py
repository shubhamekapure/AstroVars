from timezonefinder import TimezoneFinder
import pytz
from datetime import datetime


def get_timezone_name(lat, lon):
    tf = TimezoneFinder()
    return tf.timezone_at(lng=lon, lat=lat)


def local_to_utc(dt_local, tz_name):
    tz = pytz.timezone(tz_name)
    local_dt = tz.localize(dt_local)
    return local_dt.astimezone(pytz.utc)
