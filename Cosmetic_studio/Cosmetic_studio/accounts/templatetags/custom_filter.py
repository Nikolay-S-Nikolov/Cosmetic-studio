from django import template

register = template.Library()


@register.filter
def placeholder(value, arg):
    value.field.widget.attrs["placeholder"] = arg
    return value
