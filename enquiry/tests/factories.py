"""Factories for the ``enquiry`` app."""
import factory

from enquiry.models import (
    Enquiry,
    EnquiryTrans,
)


# Here is a suggestion on how to deal with multilingual model factories:

class EnquiryFactory(factory.Factory):
    """Factory for the ``Enquiry`` model."""
    FACTORY_FOR = Enquiry

    # add fields here


class EnquiryTransFactoryBase(factory.Factory):
    """Base factory for factories for ``EnquiryTrans`` models."""
    FACTORY_FOR = EnquiryTrans

    enquiry = factory.SubFactory(Enquiry)


class EnquiryTransENFactory(EnquiryTransFactoryBase):
    """Factory for english ``EnquiryTrans`` objects."""
    question = 'A question?'
    language = 'en'


class EnquiryTransDEFactory(EnquiryTransFactoryBase):
    """Factory for german ``EnquiryTrans`` objects."""
    question = 'Eine Frage?'
    language = 'de'
