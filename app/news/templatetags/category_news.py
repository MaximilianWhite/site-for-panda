from django import template
from django.db.models import Count

from news.models import Category

register = template.Library()

@register.simple_tag(name='get_list_categories')
def get_categories():
    categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)
    return categories
