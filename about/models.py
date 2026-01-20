from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

class AboutPage(Page):
    # Detailed Biography
    bio = RichTextField(
        blank=True,
        features=['h3', 'h4', 'bold', 'italic', 'link', 'ul', 'ol'],
        help_text="The detailed life story and artistic journey."
    )

    # Honors & Awards (List of items)
    honors = StreamField([
        ('honor', blocks.StructBlock([
            ('title', blocks.CharBlock(required=True, help_text="Title of the award or honor")),
            ('year', blocks.CharBlock(required=False, help_text="Year received")),
            ('organization', blocks.CharBlock(required=False, help_text="Awarding organization")),
        ])),
    ], use_json_field=True, blank=True, help_text="List of honors and awards")

    # Studio Introduction (Gallery of images mainly)
    studio_images = StreamField([
        ('image', ImageChooserBlock()),
    ], use_json_field=True, blank=True, help_text="Photos of the studio")

    content_panels = Page.content_panels + [
        FieldPanel('bio'),
        FieldPanel('honors'),
        FieldPanel('studio_images'),
    ]

    parent_page_types = ['home.HomePage']
