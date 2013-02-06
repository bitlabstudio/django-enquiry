"""URLs for the ``event_rsvp`` app."""
from django.conf.urls.defaults import patterns, url

from enquiry.views import EnquiryDetailView, VoteSubmitView


urlpatterns = patterns(
    '',
    url(r'^(?P<enquiry_pk>\d+)/$',
        VoteSubmitView.as_view(),
        name='enquiry_vote'),

    url(r'^results/(?P<pk>\d+)/$',
        EnquiryDetailView.as_view(),
        name='enquiry_detail'),
)
