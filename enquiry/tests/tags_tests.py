"""Tests for tags of the ``enquiry``` application."""
from django.test import TestCase

from enquiry.templatetags.enquiry_tags import render_current_poll
from enquiry.tests.factories import (
    AnswerTransENFactory,
    EnquiryTransENFactory,
    VoteFactory,
)


class RenderCurrentPollTestCase(TestCase):
    """Tests for the ``render_current_poll`` tag."""
    longMessage = True

    def test_tag(self):
        self.assertEqual(render_current_poll({}), '')
        self.vote = VoteFactory()
        EnquiryTransENFactory(enquiry=self.vote.answer.enquiry)
        AnswerTransENFactory(answer=self.vote.answer)
        self.assertIn('<option value="1">', render_current_poll({}))
