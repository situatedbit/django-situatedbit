from django import template

register = template.Library()

@register.inclusion_tag('pages/tags/pub_time.html')
def pub_time(date):
    return {'date': date}
