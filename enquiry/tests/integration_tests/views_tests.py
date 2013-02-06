"""Tests for views of the ``enquiry``` application."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewTestMixin

from enquiry.models import Vote
from enquiry.tests.factories import (
    AnswerTransENFactory,
    EnquiryTransENFactory,
    VoteFactory,
)


class VoteSubmitViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``VoteSubmitView`` view."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.answer_translated = AnswerTransENFactory()
        self.enquiry_translated = EnquiryTransENFactory(
            enquiry=self.answer_translated.answer.enquiry)
        self.enquiry_translated_2 = EnquiryTransENFactory()

    def get_view_name(self):
        return 'enquiry_vote'

    def get_view_kwargs(self):
        return {'enquiry_pk': self.enquiry_translated.enquiry.pk}

    def test_view(self):
        self.is_not_callable()
        data = {'answer': 'abc'}
        self.is_not_callable(method='post', data=data,
                             kwargs={'enquiry_pk': 999})
        self.is_not_callable(method='post', data=data)
        self.login(self.user)
        self.is_not_callable(method='post', data=data)
        data.update({'answer': 999})
        self.is_not_callable(method='post', data=data)
        data.update({'answer': self.answer_translated.pk})
        self.is_not_callable(method='post', data=data, kwargs={
            'enquiry_pk': self.enquiry_translated_2.pk})
        self.is_callable(method='post', data=data)
        self.assertEqual(Vote.objects.all().count(), 1)
        self.client.logout()
        self.enquiry_translated.enquiry.allow_anonymous = True
        self.enquiry_translated.enquiry.save()
        self.is_callable(method='post', data=data)
        self.assertEqual(Vote.objects.all().count(), 2)


class EnquiryDetailViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``EnquiryDetailView`` view."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.answer = AnswerTransENFactory()
        self.enquiry = EnquiryTransENFactory(
            enquiry=self.answer.answer.enquiry)

    def get_view_name(self):
        return 'enquiry_detail'

    def get_view_kwargs(self):
        return {'pk': self.enquiry.enquiry.pk}

    def test_view(self):
        self.is_not_callable()
        self.is_not_callable(user=self.user)
        VoteFactory(answer=self.answer.answer, user=self.user)
        self.is_callable(user=self.user)
        self.enquiry.enquiry.allow_anonymous = True
        self.enquiry.enquiry.save()
        self.is_not_callable(user=self.user)
        VoteFactory(answer=self.answer.answer,
                    session_key=self.client.session.session_key)
        self.is_callable(user=self.user)
