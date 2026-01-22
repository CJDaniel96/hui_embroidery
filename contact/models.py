from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from modelcluster.fields import ParentalKey


class FormField(AbstractFormField):
    page = ParentalKey('ContactPage', on_delete=models.CASCADE, related_name='form_fields')


class ContactPage(AbstractEmailForm):
    intro = RichTextField(blank=True, help_text="Text above the form")
    thank_you_text = RichTextField(blank=True, help_text="Text displayed after submission")
    
    # Contact Info
    address = RichTextField(blank=True, help_text="Studio address")
    map_embed_code = models.TextField(
        blank=True, 
        help_text="Google Maps Embed HTML code"
    )

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldPanel('address'),
            FieldPanel('map_embed_code'),
        ], heading="Location Details"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email Config"),
    ]

    parent_page_types = ['home.HomePage']
