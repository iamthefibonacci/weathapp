from django.forms import ModelForm, TextInput

from .models import Weather


class WeatherForm(ModelForm):
    class Meta:
        model = Weather
        fields = ['city', 'period']
        widgets = {
            'city': TextInput(attrs={'class': 'input', 'placeholder': 'City Name'}),
            'period': TextInput(attrs={'class': 'input', 'placeholder': 'Period'})
        }
