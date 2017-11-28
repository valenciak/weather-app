from django import forms
from forecast.models import Location


class InputForm(forms.ModelForm):
    post = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Find your location...'
        }
    ))

    class Meta:
        model = Location
        fields = ('post',)
