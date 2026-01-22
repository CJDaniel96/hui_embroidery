from django.db import models
from django import forms
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, FieldRowPanel
from wagtail.snippets.models import register_snippet
from wagtail.images.models import Image
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel

@register_snippet
class WorkCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, help_text="A slug to identify posts by this category")

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Work Categories'


class WorkPage(Page):
    # Main artwork
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="The main image of the artwork"
    )
    
    # Metadata
    year = models.CharField(max_length=4, blank=True, help_text="Year of creation")
    dimensions = models.CharField(max_length=255, blank=True, help_text="Dimensions (e.g. 50cm x 50cm)")
    materials = models.CharField(max_length=255, blank=True, help_text="Materials used")
    
    # Concept
    concept = RichTextField(blank=True, help_text="The story or concept behind the work")
    
    # Categories
    categories = ParentalManyToManyField('gallery.WorkCategory', blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('main_image'),
        ], heading="Artwork Image"),
        MultiFieldPanel([
            FieldPanel('year'),
            FieldPanel('dimensions'),
            FieldPanel('materials'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Artwork Details"),
        FieldPanel('concept'),
        InlinePanel('details_images', label="Detail Images"),
    ]

    parent_page_types = ['gallery.GalleryIndexPage']


class WorkPageDetailImage(Orderable):
    page = ParentalKey(WorkPage, on_delete=models.CASCADE, related_name='details_images')
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
        related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]


class GalleryIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # Get all work pages
        all_works = self.get_children().live().specific().order_by('-first_published_at')
        
        # Filter by category
        category_slug = request.GET.get('category')
        if category_slug:
            context['selected_category'] = category_slug
            all_works = all_works.filter(workpage__categories__slug=category_slug)
            
        context['works'] = all_works
        context['categories'] = WorkCategory.objects.all()
        return context

    parent_page_types = ['home.HomePage']
    subpage_types = ['gallery.WorkPage']
