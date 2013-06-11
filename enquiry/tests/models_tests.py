"""Tests for models of the ``enquiry``` application."""
from django.test import TestCase
from django.utils import timezone

from enquiry.tests.factories import (
    AnswerFactory,
    EnquiryFactory,
    EnquiryTransDEFactory,
    EnquiryTransENFactory,
    VoteFactory,
)


class EnquiryTestCase(TestCase):
    """Tests for the ``Enquiry`` model class."""
    longMessage = True

    def setUp(self):
        self.obj = EnquiryFactory()

    def test_model(self):
        self.assertTrue(self.obj.pk)

    def test_translation(self):
        self.assertFalse(self.obj.get_translation())
        EnquiryTransDEFactory(enquiry=self.obj)
        self.assertEqual(self.obj.get_translation().question, 'Eine Frage?')
        EnquiryTransENFactory(enquiry=self.obj)
        self.assertEqual(self.obj.get_translation().question, 'A question?')

    def test_is_active(self):
        self.assertTrue(self.obj.is_active(), msg=(
            'Should be True if the campaign is up-to-date.'))
        upcoming_event = EnquiryFactory(
            start_date=timezone.now() + timezone.timedelta(days=1))
        self.assertFalse(upcoming_event.is_active(), msg=(
            'Should be False if the campaign has not started.'))


class AnswerTestCase(TestCase):
    """Tests for the ``Answer`` model class."""
    longMessage = True

    def setUp(self):
        self.obj = AnswerFactory()

    def test_model(self):
        self.assertTrue(self.obj.pk)

    def test_get_vote_count(self):
        self.assertEqual(self.obj.get_vote_count(), 0)
        VoteFactory(answer=self.obj)
        self.assertEqual(self.obj.get_vote_count(), 1)


class VoteTestCase(TestCase):
    """Tests for the ``Vote`` model class."""
    longMessage = True

    def test_model(self):
        obj = VoteFactory()
        self.assertTrue(obj.pk)
