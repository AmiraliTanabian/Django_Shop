from django import template
from django.conf import settings

from product_module.models import ProductView

register = template.Library()


@register.filter(name="price_separator")
def price_separator(value):
    """ Three-digit numbers in prices """
    return f"{value:,} تومان "


@register.simple_tag
# @register.simple_tag(takes_context=True)
def multiplication(num1, num2):
    """Multiplication for 2 integer numbers"""
    return int(num1) * int(num2)


@register.simple_tag
def slicer(value, index):
    """Slicing according the index"""
    if len(value) <= index + 1:
        return value
    return f'{value[:index]} ... '


@register.simple_tag
def default_admin_url():
    return settings.SITE_URL + "default_admin/"


@register.simple_tag
def product_view(product):
    views = ProductView.objects.filter(product=product).count()
    return views


@register.filter(name="number_separator")
def number_separator(value):
    return f'{value:,}'
