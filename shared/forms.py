from django import forms

from shared.models import MurojaatModel


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = MurojaatModel
        fields = ['title','body']

