from django.db import models
from django.utils.html import strip_tags
from modelcluster.fields import ParentalKey
from os.path import basename
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

@register_snippet
class Photo(models.Model):
    caption = RichTextField()
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
      FieldPanel('caption', classname="full"),
      ImageChooserPanel('image'),
    ]

    def __str__(self):
        return "{0} ({1})".format(self.image.title, basename(self.image.file.name))

class PhotoPlacement(Orderable, models.Model):
    page = ParentalKey('pages.PhotoPage', related_name='photo_placements')
    photo = models.ForeignKey('pages.Photo', related_name='+')

    class Meta:
        ordering = ['sort_order']
        verbose_name = "photo placement"
        verbose_name_plural = "photo placements"

    panels = [
        SnippetChooserPanel('photo'),
    ]

    def __str__(self):
        return self.page.title + " -> " + self.photo

class RichTextPage(Page):
    body = RichTextField()

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(RichTextPage, self).get_context(request, *args, **kwargs)

        context['parent'] = self.get_parent()

        return context

class PhotoPage(RichTextPage):
    preview_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = RichTextPage.content_panels + [
        InlinePanel('photo_placements', label="Photos"),
    ]

    promote_panels = RichTextPage.promote_panels + [
        ImageChooserPanel('preview_image'),
    ]

    def preview_text(self):
        max_length = 140
        body = strip_tags(self.body)
        body_text = body if len(body) <= max_length else body[:max_length] + "…"

        return self.search_description or body_text

    def photos(self):
        return map(lambda p: p.photo, self.photo_placements.all())
