from django import forms

from . import models


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        fields = ('avatar', 'first_name', 'last_name', 'bio')
        model = models.UserProfile