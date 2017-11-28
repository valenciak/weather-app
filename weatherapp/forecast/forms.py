from django import forms
from forecast.models import Weather


class InputForm(forms.ModelForm):
    post = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Find your location...'
        }
    ))

    class Meta:
        model = Weather
        fields = ('post',)
