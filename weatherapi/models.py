from django.db import models


class Weather(models.Model):
    city = models.CharField(max_length=25)
    period = models.IntegerField()

    class Meta:
        verbose_name_plural = 'weather'

