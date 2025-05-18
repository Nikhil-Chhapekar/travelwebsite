from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def split(value, delimiter):
    """Split a string by delimiter and return the list"""
    if value:
        if isinstance(value, str):
            return value.split(delimiter)
        else:
            # Handle timeuntil values by converting to string first
            return str(value).split(delimiter)
    return []

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return Decimal(str(value)) * Decimal(str(arg))
    except (ValueError, TypeError):
        return 0

@register.filter
def days_until(value, arg):
    """Extract days from timeuntil filter result"""
    try:
        from django.utils.timezone import now
        from django.utils.timesince import timeuntil

        # If arg is now, calculate timeuntil from value to now
        if arg == 'now':
            time_str = timeuntil(value, now())
        else:
            time_str = timeuntil(value, arg)

        # Extract days from timeuntil string
        if 'day' in time_str:
            days_str = time_str.split(',')[0]
            return int(days_str.split()[0])
        return 0
    except Exception:
        return 0
