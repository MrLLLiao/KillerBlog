import markdown2
from django import template

register = template.Library()


@register.filter
def markdown(value):
    if not value:
        return ''
    return markdown2.markdown(value, extras=["fenced-code-blocks", "tables"])
