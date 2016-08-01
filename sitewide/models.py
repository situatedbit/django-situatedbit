from django.db import models
from django.utils.html import strip_tags

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet


@register_snippet
class FooterLink(models.Model):
    url = models.URLField()
    text = models.CharField(max_length=255)
    title = models.CharField(blank=True, max_length=512)

    panels = [
        FieldPanel('url'),
        FieldPanel('text'),
        FieldPanel('title'),
    ]

    def __str__(self):
        return self.text

@register_snippet
class Bio(models.Model):
    text = RichTextField()
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('text'),
        ImageChooserPanel('image'),
    ]

    def __str__(self):
        return strip_tags(self.text)

@register_snippet
class Copyright(models.Model):
    text = RichTextField()

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return strip_tags(self.text)
