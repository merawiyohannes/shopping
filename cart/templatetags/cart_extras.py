from django import template

register = template.Library()

@register.filter
def get_item(cart, key):
    try:
        return cart.get(str(key))
    except:
        return None