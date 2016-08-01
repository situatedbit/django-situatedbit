from django import template
from sitewide.models import *

register = template.Library()

@register.inclusion_tag('sitewide/tags/footer_links.html', takes_context=True)
def footer_links(context):
    return {
        'footer_links': FooterLink.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('sitewide/tags/bio.html', takes_context=True)
def bio(context):
    return {
        'bio': Bio.objects.first(),
        'request': context['request'],
    }

@register.inclusion_tag('sitewide/tags/copyright.html', takes_context=True)
def copyright(context):
    return {
        'copyright': Copyright.objects.first(),
        'request': context['request'],
    }
