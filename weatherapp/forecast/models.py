from django.db import models


class Weekdays(models.Model):
    one = models.CharField(max_length=16)
    two = models.CharField(max_length=16)
    three = models.CharField(max_length=16)
    four = models.CharField(max_length=16)
    five = models.CharField(max_length=16)
    six = models.CharField(max_length=16)
    seven = models.CharField(max_length=16)


class Weather(models.Model):
    summary = models.CharField(max_length=256)
    location = models.CharField(max_length=128)
    timestamp = models.IntegerField()
    date = models.DateField()
    temperature = models.IntegerField()
    low = models.IntegerField()
    high = models.IntegerField()
    humidity = models.IntegerField()
    weekdays = models.ForeignKey(Weekdays)
    wind_speed = models.DecimalField(max_digits=3, decimal_places=2)
    icon = models.CharField(max_length=32)


class Future(models.Model):
    two = Weather()
    three = Weather()
    four = Weather()
    five = Weather()
    six = Weather()
    seven = Weather()
