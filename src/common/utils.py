"""
Shared utility functions used across multiple modules.
"""

import re
from datetime import datetime
try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None # Fallback


def is_active_cst_window() -> bool:
    """
    Checks if the current time in CST is within the active polling window:
    - Between 11:00 PM (23:00) and 08:00 AM (07:59) CST.
    - Only during the 0-5 and 30-35 minute marks (top and half of the hour).
    This creates exactly 18 time durations per day.
    """
    try:
        tz = ZoneInfo("America/Chicago") if ZoneInfo else None
    except Exception:
        tz = None

    now = datetime.now(tz)
    hour = now.hour
    minute = now.minute

    # Are we in the allowed minute range? (allow 5 min buffer to execute)
    # Top of hour: minutes 55-59 or 0-5
    is_top_of_hour = minute >= 55 or minute <= 5
    is_half_hour = (25 <= minute <= 35)

    return is_top_of_hour or is_half_hour


def safe_id(username: str) -> str:
    """Generate a filesystem-safe unique identifier from a username/email.
    
    Replaces any character that is not alphanumeric with an underscore.
    Used for state file names, Chrome profile directories, etc.
    """
    return re.sub(r'[^a-zA-Z0-9]', '_', str(username))
