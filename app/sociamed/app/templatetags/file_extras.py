from django import template
import os

register = template.Library()

@register.filter
def is_image(filename):
    return filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
    
@register.filter
def filename(file_field):
    return os.path.basename(file_field.name)