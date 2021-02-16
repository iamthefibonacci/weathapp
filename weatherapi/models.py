from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Weather(models.Model):
    city = models.CharField(max_length=25)
    period = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(3)])

    class Meta:
        verbose_name_plural = 'weather'


