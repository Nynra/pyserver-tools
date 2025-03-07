from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter
def is_in_group(user, group_name):
    """Check if the user is in the given group"""
    if user.is_authenticated:
        return user.groups.filter(name=group_name).exists()
    return False
