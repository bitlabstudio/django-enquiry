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
        # 404: No post data
        self.is_not_callable()

        # 404: Enquiry not found
        data = {'answer': 'abc'}
        self.is_not_callable(method='post', data=data,
                             kwargs={'enquiry_pk': 999})

        # 404: Not logged in (enquiry disallows anonymous votes)
        self.is_not_callable(method='post', data=data)

        # 404: Posted answer id not int()
        self.login(self.user)
        self.is_not_callable(method='post', data=data)

        # 404: Answer not found
        data.update({'answer': 999})
        self.is_not_callable(method='post', data=data)

        # 404: Answer doesn't match the enquiry
        data.update({'answer': self.answer_translated.pk})
        self.is_not_callable(method='post', data=data, kwargs={
            'enquiry_pk': self.enquiry_translated_2.pk})

        # 200: Answer matches enquiry
        self.is_callable(method='post', data=data)
        self.assertEqual(Vote.objects.all().count(), 1)
        self.assertEqual(Vote.objects.all()[0].user, self.user)
        self.assertEqual(Vote.objects.all()[0].session_key,
                         self.client.session.session_key)

        # 200: Anonymous vote allowed
        self.enquiry_translated.enquiry.allow_anonymous = True
        self.enquiry_translated.enquiry.save()
        self.is_callable(method='post', data=data, anonymous=True)
        self.assertEqual(Vote.objects.all().count(), 2)
        self.assertFalse(Vote.objects.all()[1].user)


class EnquiryDetailViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``EnquiryDetailView`` view."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.answer = AnswerTransENFactory()
        self.enquiry = EnquiryTransENFactory(
            enquiry=self.answer.answer.enquiry)
        self.user_2 = UserFactory()

    def get_view_name(self):
        return 'enquiry_detail'

    def get_view_kwargs(self):
        return {'pk': self.enquiry.enquiry.pk}

    def test_view(self):
        # 404: Anonymous has no votes and anonymous vote is disabled
        self.is_not_callable()

        # 404: User has no votes
        self.is_not_callable(user=self.user)

        # 200: User has a vote
        session_key = self.client.session.session_key
        VoteFactory(answer=self.answer.answer, user=self.user,
                    session_key=session_key)
        self.is_callable(user=self.user)

        self.enquiry.enquiry.allow_anonymous = True
        self.enquiry.enquiry.save()

        # 404: Anonymous has no vote, cause session_key is lost through logout
        self.client.logout()
        self.is_not_callable()
