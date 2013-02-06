"""Models for the ``enquiry`` app."""
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _

from simple_translation.utils import get_translation_queryset


class TransModelMixin(object):
    """Mixin that returns the translation object for a given parent model."""
    def get_translation(self):
        lang = get_language()
        queryset = get_translation_queryset(self).filter(language=lang)
        if queryset:
            return queryset[0]
        # If there's no translation available in the current language
        queryset = get_translation_queryset(self)
        if queryset:
            return queryset[0]
        # If there's no translation available at all
        return None


class Enquiry(TransModelMixin, models.Model):
    """
    An enquiry has start and end dates and a question with several answers.

    For translateable fields see the ``EnquiryTrans`` model.

    :creation_date: The DateTime when this enquiry was created.
    :created_by: The user who created this enquiry.
    :start_date: The start date of this enquiry.
    :end_date: The end date of this enquiry.
    :allow_anonymous: If ``True`` anonymous user can participate, otherwise
      users must be authenticated in order to vote.

    """
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation Date'),
    )

    created_by = models.ForeignKey(
        'auth.User',
        verbose_name=_('Created by'),
        related_name='enquiries',
    )

    start_date = models.DateTimeField(
        default=timezone.now(),
        verbose_name=_('Start'),
    )

    end_date = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(days=7),
        verbose_name=_('End'),
    )

    allow_anonymous = models.BooleanField(
        default=False,
        verbose_name=_('Allow anonymous votes'),
    )

    def __unicode__(self):
        translation = self.get_translation()
        if translation:
            return translation.question
        return 'not translated'


class EnquiryTrans(models.Model):
    """
    Translateable fields for the ``Enquiry`` model.

    :question: The title of this category.

    """
    question = models.CharField(
        max_length=100,
        verbose_name=_('Question'),
    )

    # Needed by simple-translation
    enquiry = models.ForeignKey(Enquiry, verbose_name=_('Enquiry'))
    language = models.CharField(
        max_length=2, verbose_name=_('Language'), choices=settings.LANGUAGES)

    def __unicode__(self):
        return self.question

    def get_answers(self):
        """Returns a queryset of all answers to its question."""
        return [answer for answer in self.enquiry.answers.all()]


class Answer(TransModelMixin, models.Model):
    """
    An answer belongs to an enquiry.

    For translateable fields see ``AnswerTrans`` model.

    :enquiry: FK to the enquiry this answer belongs to.

    """
    enquiry = models.ForeignKey(
        'enquiry.Enquiry',
        verbose_name=_('Enquiry'),
        related_name='answers',
    )

    def __unicode__(self):
        translation = self.get_translation()
        if translation:
            return translation.text
        return 'not translated'

    def get_vote_count(self):
        """Returns the number of votes for this answer."""
        return self.votes.all().count()


class AnswerTrans(models.Model):
    """
    Translateable fields for the ``Answer`` model.

    :text: The text of this answer.

    """
    text = models.CharField(
        max_length=100,
        verbose_name=_('Answer'),
    )

    # Needed by simple-translation
    answer = models.ForeignKey(Answer, verbose_name=_('Answer'))
    language = models.CharField(
        max_length=2, verbose_name=_('Language'), choices=settings.LANGUAGES)

    def __unicode__(self):
        return '{0} - {1}'.format(self.answer.enquiry, self.text)


class Vote(models.Model):
    """
    A vote is being cast on an answer by a user.

    :answer: The answer this user has chosen.
    :user: The user who cast this vote. Can be None if the user was anonymous.

    We also need to save something to identify anonymous users here. IP might
    not be a good idea because those students might all access the portal
    from within the campus and have the same IP.

    Maybe we are saving sessions in the database and we could save the session
    PK here? But we are cleaning up the sessions regularily, so then the
    PKs in this field would no longer be valid. Can't remember how we did this
    with the FAQ app, please come up with a good idea.

    """
    answer = models.ForeignKey(
        'enquiry.Answer',
        verbose_name=_('Answer'),
        related_name='votes',
    )

    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
        related_name='votes',
    )

    def __unicode__(self):
        return self.answer
