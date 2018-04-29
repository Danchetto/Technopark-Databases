from datetime import datetime, date
from tzlocal import get_localzone
import pytz
import json


def normalize_time(time):
    return datetime.timestamp(datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f%Z"))

# def time_to_str(time):
#     time = arrow.get(time, )
#
#     time.to('local')
#     return time.isoformat() date


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        local_tz = get_localzone()
        if isinstance(o, datetime):
            return o.replace(tzinfo=pytz.utc).astimezone(local_tz).isoformat()
        elif isinstance(o, date):
            return o.isoformat()
        elif isinstance(o, str):
            return o
        else:
            return super(DateTimeEncoder, self).default(o)


def date_converter(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()


def time_to_str(time):
    return time.isoformat()


def get_time():
    local_tz = get_localzone()
    return datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(local_tz).isoformat()
    # return datetime.now().isoformat()
