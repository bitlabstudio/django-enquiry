"""Views for the ``event_rsvp`` app."""
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic import DetailView, CreateView

from enquiry.forms import VoteForm
from enquiry.models import Answer, Enquiry, Vote


class VoteSubmitView(CreateView):
    """View to create a new vote instance."""
    model = Vote
    form_class = VoteForm

    def dispatch(self, request, *args, **kwargs):
        """Get the relevant enquiry and check if this vote can be anonymous."""
        if (not request.method == 'POST' or not request.POST.get('answer')
                or not kwargs.get('enquiry_pk')):
            raise Http404
        try:
            self.enquiry = Enquiry.objects.get(pk=kwargs.get('enquiry_pk'))
        except Enquiry.DoesNotExist:
            raise Http404
        else:
            if (not self.enquiry.allow_anonymous
                    and not request.user.is_authenticated()):
                raise Http404
        try:
            answer_id = int(request.POST.get('answer'))
        except ValueError:
            raise Http404
        try:
            self.answer = Answer.objects.get(pk=answer_id)
        except Answer.DoesNotExist:
            raise Http404
        else:
            if self.answer.enquiry != self.enquiry:
                raise Http404
        return super(VoteSubmitView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self, **kwargs):
        kwargs = super(VoteSubmitView, self).get_form_kwargs(**kwargs)
        if self.request.user.is_authenticated():
            kwargs.update({'user': self.request.user})
        kwargs.update({'session_key': self.request.session.session_key})
        return kwargs

    def get_success_url(self):
        return reverse('enquiry_detail', kwargs={'pk': self.enquiry.pk})


class EnquiryDetailView(DetailView):
    """View to display a enquiry instance."""
    model = Enquiry

    def dispatch(self, request, *args, **kwargs):
        self.kwargs = kwargs
        self.object = self.get_object()
        if (not self.object.allow_anonymous
                and not request.user.is_authenticated()):
            raise Http404
        if self.object.has_voted(request):
            return super(EnquiryDetailView, self).dispatch(request, *args,
                                                           **kwargs)
        raise Http404

    def get_context_data(self, **kwargs):
        context = super(EnquiryDetailView, self).get_context_data(**kwargs)
        context.update({'enquiry_translated': self.object.get_translation()})
        return context
