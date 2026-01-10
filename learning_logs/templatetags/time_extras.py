from datetime import datetime, timezone
from django import template

register = template.Library()


@register.filter
def rough_timesince(date):
    """
    Возвращает 'X seconds', 'X minutes', 'X hours', 'X days', 'X weeks', 'X months', 'X years'
    только с самой крупной единицей.
    """
    if not date:
        return ""

    now = datetime.now(timezone.utc) if date.tzinfo else datetime.now()
    if date.tzinfo:
        diff = now - date
    else:
        diff = now.replace(tzinfo=None) - date

    seconds = int(diff.total_seconds())
    if seconds < 0:
        return "just now"

    if seconds < 60:
        return f"{seconds} second{'s' if seconds != 1 else ''}"
    elif seconds < 3600:  # < 1 hour
        minutes = seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    elif seconds < 86400:  # < 1 day
        hours = seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''}"
    elif seconds < 604800:  # < 1 week
        days = seconds // 86400
        return f"{days} day{'s' if days != 1 else ''}"
    elif seconds < 2592000:  # < 1 month (~30 days)
        weeks = seconds // 604800
        return f"{weeks} week{'s' if weeks != 1 else ''}"
    elif seconds < 31536000:  # < 1 year
        months = seconds // 2592000
        return f"{months} month{'s' if months != 1 else ''}"
    else:
        years = seconds // 31536000
        return f"{years} year{'s' if years != 1 else ''}"
