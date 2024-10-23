from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def time_difference(current_time, previous_time):
	delta = (current_time - previous_time).total_seconds()
	return delta

@register.filter
def index(lst, i):
    """Return the item at index `i` in list `lst`, or None if out of range."""
    try:
        return lst[i]
    except IndexError:
        return None