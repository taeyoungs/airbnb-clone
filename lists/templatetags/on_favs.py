from django import template
from lists import models as list_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, room):

    user = context.request.user
    try:
        the_list = user.list.room.all()
        if room in the_list:
            return True
    except list_models.List.DoesNotExist:
        return False
