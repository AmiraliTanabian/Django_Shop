from django import template
from django.db.models.fields import return_None

from site_module.models import SiteSetting

register = template.Library()


@register.inclusion_tag("admin_module/components/navbar.html", name="admin_navbar_inclution", takes_context=True)
def admin_navbar_inclution(context, *args, **kwargs):
    user = context["request"].user
    current_site_setting = SiteSetting.objects.filter(is_active=True).first()
    context = {
        "site_setting": current_site_setting,
        "user": user,
    }
    return context
