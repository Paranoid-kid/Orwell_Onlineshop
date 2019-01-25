from django import template

register = template.Library()


@register.filter
def to_and(value):
    value = value.replace("&", "-")
    value = value.replace("|", "\n")
    return value
