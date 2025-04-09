from django import template

register = template.Library()

@register.filter(name="price_separator")
def price_separator(value):
    """ Three-digit numbers in prices """
    return f"{value:,} تومان "