"""Tests for forms of the ``enquiry``` application."""
from django.test import TestCase

from enquiry.forms import VoteForm
from enquiry.models import Vote
from enquiry.tests.factories import AnswerFactory


class VoteFormTestCase(TestCase):
    """Tests for the ``VoteForm`` form."""
    longMessage = True

    def test_form(self):
        form = VoteForm(data={'answer': AnswerFactory().id},
                        session_key='a1b2c3d4e5')
        self.assertTrue(form.is_valid(), msg=('{0}'.format(form.errors)))
        form.save()
        self.assertEqual(Vote.objects.all().count(), 1)
