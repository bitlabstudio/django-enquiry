"""Admin classes for the ``enquiry`` app."""
from django.contrib import admin

from simple_translation.admin import TranslationAdmin

from enquiry.models import Answer, Enquiry, Vote


class AnswerAdmin(TranslationAdmin):
    pass


class EnquiryAdmin(TranslationAdmin):
    list_display = [
        'question', 'start_date', 'end_date', 'is_published', 'languages', ]

    def question(self, obj):
       return obj.get_translation().question


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Enquiry, EnquiryAdmin)
admin.site.register(Vote)
