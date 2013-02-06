"""Forms for the ``enquiry`` app."""
from django import forms

from enquiry.models import Vote


class VoteForm(forms.ModelForm):
    """Form to create a new vote."""
    def __init__(self, user=None, session_key=None, *args, **kwargs):
        self.user = user
        self.session_key = session_key
        super(VoteForm, self).__init__(*args, **kwargs)

    def save(self, **kwargs):
        self.instance.user = self.user
        if self.session_key:
            self.instance.session_key = self.session_key
        return super(VoteForm, self).save(**kwargs)

    class Meta:
        model = Vote
        fields = ('answer', )
