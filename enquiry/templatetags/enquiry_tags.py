"""Template tags for the ``enquiry`` app."""
from django import template
from django.utils.timezone import now

from enquiry.models import Enquiry

register = template.Library()


@register.simple_tag(takes_context=True)
def render_current_poll(context):
    """Template tag to render the current poll."""
    enquiries = Enquiry.objects.filter(start_date__lt=now(),
                                       end_date__gt=now())
    if enquiries:
        translation = enquiries[0].get_translation()
        return template.loader.render_to_string(
            'enquiry/current_poll.html',
            {'enquiry_translated': translation,
             'has_voted': enquiries[0].has_voted(context['request'])},
            context)
    return ''
