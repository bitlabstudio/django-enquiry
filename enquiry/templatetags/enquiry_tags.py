"""Template tags for the ``enquiry`` app."""
from django import template
from django.utils.timezone import now

from enquiry.models import Enquiry

register = template.Library()


@register.simple_tag()
def render_current_poll():
    """Template tag to render the current poll."""
    enquiries = Enquiry.objects.filter(start_date__lt=now(),
                                       end_date__gt=now())
    if enquiries:
        translation = enquiries[0].get_translation()
        return template.loader.render_to_string('enquiry/current_poll.html',
                                                {'enquiry': translation})
    return ''
