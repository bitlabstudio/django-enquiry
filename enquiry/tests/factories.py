"""Factories for the ``enquiry`` app."""
from django.utils import timezone

from django_libs.tests.factories import UserFactory
import factory

from enquiry import models


class EnquiryFactory(factory.Factory):
    """Factory for the ``Enquiry`` model."""
    FACTORY_FOR = models.Enquiry

    created_by = factory.SubFactory(UserFactory)
    start_date = factory.LazyAttribute(
        lambda a: timezone.now() - timezone.timedelta(days=1))
    end_date = factory.LazyAttribute(
        lambda a: timezone.now() + timezone.timedelta(days=7))


class EnquiryTransFactoryBase(factory.Factory):
    """Base factory for factories for ``EnquiryTrans`` models."""
    FACTORY_FOR = models.EnquiryTrans

    enquiry = factory.SubFactory(EnquiryFactory)


class EnquiryTransENFactory(EnquiryTransFactoryBase):
    """Factory for english ``EnquiryTrans`` objects."""
    question = 'A question?'
    language = 'en'


class EnquiryTransDEFactory(EnquiryTransFactoryBase):
    """Factory for german ``EnquiryTrans`` objects."""
    question = 'Eine Frage?'
    language = 'de'


class AnswerFactory(factory.Factory):
    """Factory for the ``Answer`` model."""
    FACTORY_FOR = models.Answer

    enquiry = factory.SubFactory(EnquiryFactory)


class AnswerTransFactoryBase(factory.Factory):
    """Base factory for factories for ``EnquiryTrans`` models."""
    FACTORY_FOR = models.AnswerTrans

    answer = factory.SubFactory(AnswerFactory)


class AnswerTransENFactory(AnswerTransFactoryBase):
    """Factory for english ``AnswerTrans`` objects."""
    text = 'An answer'
    language = 'en'


class AnswerTransDEFactory(AnswerTransFactoryBase):
    """Factory for german ``AnswerTrans`` objects."""
    text = 'Eine Antwort'
    language = 'de'


class VoteFactory(factory.Factory):
    """Factory for the ``Answer`` model."""
    FACTORY_FOR = models.Vote

    answer = factory.SubFactory(AnswerFactory)
    user = factory.SubFactory(UserFactory)
