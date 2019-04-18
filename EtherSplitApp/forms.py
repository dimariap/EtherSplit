from django import forms
from django.contrib.auth.models import Group
from EtherSplitApp.models import Session


class NewSessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['name', 'group', 'description']

    name = forms.CharField(required=True, max_length=64)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    description = forms.CharField(
       required=False,
       widget=forms.Textarea
    )
