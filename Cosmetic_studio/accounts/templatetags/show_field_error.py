from django import template

register = template.Library()


@register.inclusion_tag("accounts/form_field_errors.html")
def render_field_errors(field):
    return {
        "field": field,
    }
