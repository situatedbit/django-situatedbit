from django import template

register = template.Library()

@register.inclusion_tag('pages/tags/pagination_next.html')
def paginate_next(pages):
    return {'next': pages}

@register.inclusion_tag('pages/tags/pagination_previous.html')
def paginate_previous(pages):
    return {'pages': pages}
