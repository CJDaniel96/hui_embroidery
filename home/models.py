from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.models import Image


class HomePage(Page):
    # Hero Section
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Full screen hero image for the homepage"
    )
    
    # Intro Section
    intro_title = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="Main heading for the introduction (e.g., 'National Art Master')"
    )
    intro_text = RichTextField(
        blank=True, 
        help_text="Short bio or introduction text"
    )

    # Content Panels
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_image'),
        ], heading="Hero Section"),
        MultiFieldPanel([
            FieldPanel('intro_title'),
            FieldPanel('intro_text'),
        ], heading="Introduction"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        
        # Get latest works from Gallery
        # We use a deferred import to avoid circular dependency issues if any exist,
        # though ideally we are at the leaf node here.
        # But standard import at top is better if possible. 
        # Checking imports above, we need to add them.
        
        from gallery.models import WorkPage, GalleryIndexPage
        from about.models import AboutPage
        from contact.models import ContactPage

        # Gallery Context
        # Fetch up to 6 latest published works
        context['latest_works'] = WorkPage.objects.live().public().order_by('-first_published_at')[:6]
        context['gallery_index'] = GalleryIndexPage.objects.live().public().first()

        # About Context
        context['about_page'] = AboutPage.objects.live().public().first()

        # Contact Context
        context['contact_page'] = ContactPage.objects.live().public().first()

        return context
