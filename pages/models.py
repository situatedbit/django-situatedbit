from django.db import models
from django.utils.html import strip_tags
from modelcluster.fields import ParentalKey
from os.path import basename
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, Orderable, PageManager, PageQuerySet
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

class BasePage(Page):
    preview_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def preview_text(self):
        return self.search_description

    promote_panels = Page.promote_panels + [
        ImageChooserPanel('preview_image'),
    ]

class Pagination:
    pagination_param = 'p'

    # requires previews_query, previews_per_page, previews

    def pages(self, page_request):
        request = Pagination.Request(page_request, self.previews_query(), self.previews_per_page, Pagination.pagination_param)

        return {
            'next_page': request.next_page(),
            'previous_page': request.previous_page(),
            'previews': self.previews(self.previews_query()) #[request.query_min(), request.query_max()])
        }

    class Request:
        def __init__(self, request, query, previews_per_page, param):
            self.request = request
            self.query = query
            self.previews_per_page = previews_per_page
            self.param = param

        def current_page(self):
            page_arg = int(self.request.GET.get(self.param, 1))
            return min(self.pages_count(), max(1, page_arg))

        def next_page(self):
            current_page = self.current_page()
            return {'url': self.paginated_url(current_page + 1)} if current_page < self.pages_count() else None

        def pages_count(self):
            self._pages_count = self.query.count()
            return self._pages_count

        def paginated_url(self, page):
            return "?{0}={1}".format(self.param, page)

        def previous_page(self):
            current_page = self.current_page()
            return {'url': self.paginated_url(current_page - 1) } if current_page > 1 else None

        def query_min(self):
            return (self.current_page() - 1) * self.previews_per_page

        def query_max(self):
            return self.query_min() + self.previews_per_page

class IndexPage(BasePage, Pagination):
    previews_per_page = models.IntegerField(default=5, blank=False)

    def get_context(self, request):
        context = super(IndexPage, self).get_context(request)
        context['pages'] = self.pages(request)
        return context

    def previews_query(self):
        return self.get_children().order_by('-first_published_at').live()

    def previews(self, query):
        return map(lambda p: Preview(p.specific), query)

class HomePage(IndexPage):
    stream = models.ForeignKey(
        'pages.Stream',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = IndexPage.content_panels + [
        SnippetChooserPanel('stream'),
    ]

    template = 'pages/index_page.html'

    class Meta:
        verbose_name = "Home Page"

    def previews_query(self):
        # it would be better to include this in the original query, but we can't
        #if self.stream:
            #return BasePage.objects.order_by('-first_published_at').live().filter(stream=self.stream)
        #else:
        return BasePage.objects.order_by('-first_published_at').live()
        #end
#        return  BasePage.objects.descendant_of(self).not_type(IndexPage).order_by('-first_published_at').in_home_stream().live()
#        return filter(lambda p: p.specific.in_home_stream, query_set)

class Preview:
    def __init__(self, page):
        self.page = page

    def date(self):
        return self.page.first_published_at

    def has_thumbnail_class(self):
        return 'has-thumbnail' if self.page.preview_image else ''

    def text(self):
        return self.page.preview_text()

    def image(self):
        return self.page.preview_image

    def title(self):
        return self.page.title

    def url(self):
        return self.page.url

class PhotoPresenter:
    def orientation_class(self):
        return 'horizontal' if self.image.width >= self.image.height else 'vertical'

class PhotoIndexPage(IndexPage):
    subpage_types = ['pages.PhotoPage']

    template = IndexPage.template

    def previews_query(self):
        return PhotoPage.by_publish_date().descendant_of(self).live()

    def previews(self, query):
        return map(lambda p: Preview(p), query)

@register_snippet
class Photo(models.Model, PhotoPresenter):
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

@register_snippet
class Stream(models.Model):
    name = models.CharField(blank=False,max_length=255)

    panels = [
        FieldPanel('name', classname="full"),
    ]

    def __str__(self):
        return self.name + " Stream"

class StreamInclusion(models.Model):
    page = ParentalKey(Page, related_name='streams')
    stream = models.ForeignKey('pages.Stream', related_name='+')

    panels = [
        SnippetChooserPanel('stream'),
    ]

    def __str__(self):
        return "{0} <-> {1}".format(self.stream, self.page.title)

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

class RichTextPage(BasePage):
    body = RichTextField()

    search_fields = BasePage.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = BasePage.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(RichTextPage, self).get_context(request, *args, **kwargs)

        context['parent'] = self.get_parent()

        return context

    def preview_text(self):
        max_length = 140
        body = strip_tags(self.body)
        body_text = body if len(body) <= max_length else body[:max_length] + "…"

        return self.search_description or body_text

class PhotoPage(RichTextPage):
    content_panels = RichTextPage.content_panels + [
        InlinePanel('photo_placements', label="Photos"),
    ]

    def photos(self):
        return map(lambda p: p.photo, self.photo_placements.all())

    def by_publish_date():
        return PhotoPage.objects.order_by('-first_published_at')
