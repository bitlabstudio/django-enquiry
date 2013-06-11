"""URLs for the ``event_rsvp`` app."""
from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView

from .models import Enquiry
from .views import EnquirySubmitView


urlpatterns = patterns(
    '',
    url(r'^(?P<pk>\d+)/$',
        EnquirySubmitView.as_view(),
        name='enquiry_detail'),

    url(r'^$',
        ListView.as_view(model=Enquiry),
        name='enquiry_list'),
)
