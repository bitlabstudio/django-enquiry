"""Tests for tags of the ``enquiry``` application."""
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.template.context import RequestContext
from django.test import TestCase
from django.test.client import RequestFactory

from ..templatetags.enquiry_tags import get_current_poll, render_current_poll
from enquiry.tests.factories import (
    AnswerTransENFactory,
    EnquiryTransENFactory,
    VoteFactory,
)


class RenderCurrentPollTestCase(TestCase):
    """Tests for the ``render_current_poll`` tag."""
    longMessage = True

    def test_tag(self):
        # create context mock
        request = RequestFactory().get('/')
        request.user = AnonymousUser()
        SessionMiddleware().process_request(request)
        request.session.save()
        context = RequestContext(request)

        # Returns empty string if there's no current poll
        self.assertEqual(render_current_poll(context), '')

        # Returns current_poll.html
        self.vote = VoteFactory()
        enquiry_translated = EnquiryTransENFactory(
            enquiry=self.vote.answer.enquiry)
        AnswerTransENFactory(answer=self.vote.answer)
        self.assertEqual(render_current_poll(context), {
            'has_voted': False,
            'enquiry': enquiry_translated.enquiry,
        })


class GetCurrentPollTestCase(TestCase):
    """Tests for the ``get_current_poll`` tag."""
    longMessage = True

    def test_tag(self):
        # Returns None if there's no current poll
        self.assertIsNone(get_current_poll())

        # Returns current tag
        self.vote = VoteFactory()
        enquiry_translated = EnquiryTransENFactory(
            enquiry=self.vote.answer.enquiry)
        AnswerTransENFactory(answer=self.vote.answer)
        self.assertEqual(get_current_poll(), enquiry_translated.enquiry)
