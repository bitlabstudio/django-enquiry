"""Tests for views of the ``enquiry``` application."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewTestMixin

from enquiry.models import Vote
from enquiry.tests.factories import (
    AnswerTransENFactory,
    EnquiryTransENFactory,
)


class EnquirySubmitViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``EnquirySubmitView`` view."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.answer_translated = AnswerTransENFactory()
        self.enquiry_translated = EnquiryTransENFactory(
            enquiry=self.answer_translated.answer.enquiry)
        self.enquiry_translated_2 = EnquiryTransENFactory()

    def get_view_name(self):
        return 'enquiry_detail'

    def get_view_kwargs(self):
        return {'pk': self.enquiry_translated.enquiry.pk}

    def test_view(self):
        self.is_callable()

        # 404: Not logged in (enquiry disallows anonymous votes)
        data = {'answer_pk': 'abc'}
        self.is_not_callable(method='post', data=data)

        # 404: Posted answer id not int()
        self.login(self.user)
        self.is_not_callable(method='post', data=data)

        # 404: Answer not found
        data.update({'answer_pk': 999})
        self.is_not_callable(method='post', data=data)

        # 404: Answer doesn't match the enquiry
        data.update({'answer_pk': self.answer_translated.pk})
        self.is_not_callable(method='post', data=data, kwargs={
            'pk': self.enquiry_translated_2.pk})

        # 200: Answer matches enquiry
        self.is_callable(method='post', data=data)
        self.assertEqual(Vote.objects.all().count(), 1)
        self.assertEqual(Vote.objects.all()[0].user, self.user)
        self.assertEqual(Vote.objects.all()[0].session_key,
                         self.client.session.session_key)

        # 200: User can post, but no new vote should be created
        self.is_callable(method='post', data=data)
        self.assertEqual(Vote.objects.all().count(), 1)

        # 200: User can still view the enquiry
        self.is_callable()

        # 404: Should be callable as anonymous
        self.is_not_callable(method='post', data=data, anonymous=True)

        # 200: Should be callable as anonymous
        self.is_callable(data=data, anonymous=True)
