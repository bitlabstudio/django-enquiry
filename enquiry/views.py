"""Views for the ``event_rsvp`` app."""
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic import DetailView

from .models import Answer, Enquiry, Vote


class EnquirySubmitView(DetailView):
    """Display an enquiry and gather votes."""
    model = Enquiry

    def dispatch(self, request, *args, **kwargs):
        """Get the relevant enquiry and check if this vote can be anonymous."""
        self.kwargs = kwargs
        self.object = self.get_object()
        if request.method == 'POST':
            if (not self.object.allow_anonymous
                    and not request.user.is_authenticated()):
                raise Http404
            try:
                answer_id = int(request.POST.get('answer_pk'))
            except ValueError:
                raise Http404
            try:
                self.answer = Answer.objects.get(pk=answer_id)
            except Answer.DoesNotExist:
                raise Http404
            if self.answer.enquiry != self.object:
                raise Http404
            if not self.object.has_voted(request):
                if not request.user.is_authenticated():
                    Vote.objects.create(
                        answer=self.answer,
                        session_key=request.session.session_key)
                else:
                    Vote.objects.create(
                        user=request.user, answer=self.answer,
                        session_key=request.session.session_key)
            return HttpResponseRedirect(reverse(
                'enquiry_detail', kwargs={'pk': self.object.pk}))
        return super(EnquirySubmitView, self).dispatch(request, *args,
                                                       **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(EnquirySubmitView, self).get_context_data(*args,
                                                                  **kwargs)
        if self.object.has_voted(self.request):
            context.update({'has_voted': True})
        return context
