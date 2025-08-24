# # myapp/templatetags/custom_tags.py

# from django import template
# from django.utils.text import slugify

# register = template.Library()

# @register.filter
# def get_item(dict_obj, key):
#     #return dict_obj.get(key)
#     try:
#         # For queryset, filter by id == key and return first or None
#         return dict_obj.get(key)
#     except Exception:
#         return None

# @register.filter
# def slugify_text(value):
#     return slugify(value)



# myapp/templatetags/custom_tags.py

from django import template

register = template.Library()

@register.filter
def get_item(dict_obj, key):
    #return dict_obj.get(key)
    try:
        # For queryset, filter by id == key and return first or None
        return dict_obj.filter(id=key).first()
    except Exception:
        return None
