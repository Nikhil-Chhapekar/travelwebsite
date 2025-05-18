from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def split(value, arg):
    """
    Split a string by the given delimiter and return a list.
    Usage: {{ value|split:"delimiter" }}
    """
    if value:
        return value.split(arg)
    return []

@register.filter
def star_rating(value):
    """
    Convert a numeric rating to HTML star icons.
    Usage: {{ value|star_rating }}
    """
    if not value:
        value = 0
    
    full_stars = int(value)
    half_star = False
    if value - full_stars >= 0.5:
        half_star = True
    
    stars_html = ""
    for i in range(5):
        if i < full_stars:
            stars_html += '<i class="fas fa-star text-warning"></i>'
        elif half_star and i == full_stars:
            stars_html += '<i class="fas fa-star-half-alt text-warning"></i>'
        else:
            stars_html += '<i class="far fa-star text-warning"></i>'
    
    return mark_safe(stars_html)
