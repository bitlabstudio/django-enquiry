"""Template tags for the ``enquiry`` app."""
from django import template
from django.db.models import Q
from django.utils.timezone import now

from enquiry.models import Enquiry

register = template.Library()


@register.inclusion_tag('enquiry/current_poll.html', takes_context=True)
def render_current_poll(context):
    """Template tag to render one of the current active polls."""
    enquiries = Enquiry.objects.filter(
        Q(start_date__lt=now()),
        Q(end_date__gt=now()) | Q(end_date__isnull=True))
    if enquiries:
        return {
            'enquiry': enquiries[0],
            'has_voted': enquiries[0].has_voted(context['request'])
        }
    return ''


@register.assignment_tag
def get_current_poll():
    """Returns the current active poll."""
    enquiries = Enquiry.objects.filter(
        Q(start_date__lt=now()),
        Q(end_date__gt=now()) | Q(end_date__isnull=True))
    if enquiries:
        return enquiries[0]
    return None
