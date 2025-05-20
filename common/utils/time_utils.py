import datetime

def get_current_timestamp():
    """获取当前时间戳"""
    return datetime.datetime.now()

def get_hour_start(dt=None):
    """获取指定时间的整点开始时间"""
    if dt is None:
        dt = datetime.datetime.now()
    return dt.replace(minute=0, second=0, microsecond=0)

def get_date_start(dt=None):
    """获取指定时间的日期开始时间"""
    if dt is None:
        dt = datetime.datetime.now()
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)

def format_datetime(dt, format_str='%Y-%m-%d %H:%M:%S'):
    """格式化日期时间"""
    return dt.strftime(format_str)

def get_days_ago(days=3, dt=None):
    """获取指定天数前的时间，默认为3天前"""
    if dt is None:
        dt = datetime.datetime.now()
    return dt - datetime.timedelta(days=days)