"""URLs for the ``event_rsvp`` app."""
from django.conf.urls.defaults import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^(?P<pk>\d+)/$',
        views.EnquirySubmitView.as_view(),
        name='enquiry_detail'),

    url(r'^$',
        views.EnquiryListView.as_view(),
        name='enquiry_list'),
)
