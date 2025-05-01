from django import template

register = template.Library()


@register.filter(name="price_separator")
def price_separator(value):
    """ Three-digit numbers in prices """
    return f"{value:,} تومان "


@register.simple_tag
# @register.simple_tag(takes_context=True)
def multiplication(num1, num2):
    "Multiplication for 2 integer numbers"
    return int(num1) * int(num2)
