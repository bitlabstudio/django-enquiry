"""CMS apphook for the ``enquiry`` app."""
from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class EnquiryApphook(CMSApp):
    name = _("Enquiry Apphook")
    urls = ["enquiry.urls"]


apphook_pool.register(EnquiryApphook)
