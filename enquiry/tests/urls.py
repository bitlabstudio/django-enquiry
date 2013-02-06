"""
This ``urls.py`` is only used when running the tests via ``runtests.py``.
As you know, every app must be hooked into yout main ``urls.py`` so that
you can actually reach the app's views (provided it has any views, of course).

"""
from django.conf import settings
from django.conf.urls.defaults import include, patterns, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^enquiries/', include('enquiry.urls')),
    url(r'^', TemplateView.as_view(template_name='base.html')),
)
