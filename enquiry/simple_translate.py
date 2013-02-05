"""Registration of models of the ``enquiry`` app."""
from simple_translation.translation_pool import translation_pool

from enquiry.models import (
    Answer,
    AnswerTrans,
    Enquiry,
    EnquiryTrans,
)


translation_pool.register_translation(Answer, AnswerTrans)
translation_pool.register_translation(Enquiry, EnquiryTrans)
