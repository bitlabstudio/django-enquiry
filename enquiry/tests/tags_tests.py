"""Tests for tags of the ``enquiry``` application."""
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.template.context import RequestContext
from django.test import TestCase
from django.test.client import RequestFactory

from ..templatetags.enquiry_tags import (
    get_answers,
    get_current_poll,
    render_current_poll,
)
from enquiry.tests.factories import (
    AnswerTransENFactory,
    EnquiryTransENFactory,
    VoteFactory,
)


class GetAnswersTestCase(TestCase):
    """Tests for the ``get_answers`` tag."""
    longMessage = True

    def test_tag(self):
        enquiry = EnquiryTransENFactory()
        answer1 = AnswerTransENFactory(answer__enquiry=enquiry.enquiry)
        answer2 = AnswerTransENFactory(answer__enquiry=enquiry.enquiry)
        vote = VoteFactory(answer=answer2.answer)
        result = get_answers(enquiry.enquiry)
        self.assertEqual(result[0], answer1, msg=(
            'When called without sort it should return the answers ordered by'
            ' ID (Django default)'))
        result = get_answers(enquiry.enquiry, sort=True)
        self.assertEqual(result[0], answer2, msg=(
            'When called without sort it should return the answers ordered by'
            ' vote count'))


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
