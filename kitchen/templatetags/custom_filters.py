from django import template
register = template.Library()

@register.filter
def get_item(cart, key):
    return cart.get(key, 0)
