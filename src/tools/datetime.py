from datetime import datetime

def normalize_time(time):
    return datetime.timestamp(datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ"))

def time_to_str(time):
    return datetime.isoformat(time)
