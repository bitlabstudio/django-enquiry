"""Models for the ``enquiry`` app."""
from django.conf import settings
from django.db import models
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _

from simple_translation.utils import get_translation_queryset


class TransModelMixin(object):
    """Mixin that returns the translation object for a given parent model."""
    def get_translation(self):
        lang = get_language()
        return get_translation_queryset(self).filter(language=lang)[0]


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
    def __unicode__(self):
        return self.get_translation().question


class EnquiryTrans(models.Model):
    """
    Translateable fields for the ``Enquiry`` model.

    :question: The title of this category.

    """
    # Needed by simple-translation
    enquiry = models.ForeignKey(Enquiry, verbose_name=_('Enquiry'))
    language = models.CharField(
        max_length=2, verbose_name=_('Language'), choices=settings.LANGUAGES)


class Answer(models.Model):
    """
    An answer belongs to an enquiry.

    For translateable fields see ``AnswerTrans`` model.

    :enquiry: FK to the enquiry this answer belongs to.

    """
    pass

    def __unicode__(self):
        return self.get_translation().text

    def get_vote_count(self):
        """Returns the number of votes for this answer."""
        pass


class AnswerTrans(models.Model):
    """
    Translateable fields for the ``Answer`` model.

    :text: The text of this answer.

    """
    # Needed by simple-translation
    answer = models.ForeignKey(Answer, verbose_name=_('Answer'))
    language = models.CharField(
        max_length=2, verbose_name=_('Language'), choices=settings.LANGUAGES)


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
    pass
