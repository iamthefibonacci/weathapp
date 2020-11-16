from django.forms import ModelForm, TextInput, NumberInput

from .models import Weather


class WeatherForm(ModelForm):
    class Meta:
        model = Weather
        fields = ['city', 'period']
        widgets = {
            'city': TextInput(attrs={'class': 'input', 'placeholder': 'City', 'required': True}),
            'period': NumberInput(attrs={'class': 'input', 'placeholder': 'Period','min': 1, 'max': 3, 'required': True, 'type': 'number'}),
        }
