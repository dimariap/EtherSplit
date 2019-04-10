from django import forms
from django.contrib.auth.models import Group


class NewSessionForm(forms.Form):
    session_name = forms.CharField(required=True, max_length=64)
    session_group = forms.ModelMultipleChoiceField(queryset=Group.objects.all().order_by('name'), required=True)
    session_description = forms.CharField(
        required=False,
        widget=forms.Textarea
    )
