from django.db import models


class Location(models.Model):
    location = models.IntegerField(max_length=128)


class Weather(models.Model):
    location = models.ForeignKey(Location)
    timestamp = models.DateTimeField()
    temperature = models.IntegerField()
    humidity = models.IntegerField()
    wind_speed = models.DecimalField(max_digits=3, decimal_places=2)
