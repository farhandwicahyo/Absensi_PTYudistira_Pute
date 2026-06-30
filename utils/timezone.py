"""
Utility timezone untuk WIB (UTC+7)
"""
from datetime import datetime, date, timedelta, timezone
from config import Config

try:
    from zoneinfo import ZoneInfo
    WIB_TZ = ZoneInfo(Config.TIMEZONE)
except Exception:
    WIB_TZ = timezone(timedelta(hours=Config.TIMEZONE_OFFSET_HOURS))


def now_wib():
    """Waktu saat ini dalam WIB (naive datetime untuk penyimpanan DB)."""
    return datetime.now(WIB_TZ).replace(tzinfo=None)


def today_wib():
    """Tanggal hari ini dalam WIB."""
    return datetime.now(WIB_TZ).date()
