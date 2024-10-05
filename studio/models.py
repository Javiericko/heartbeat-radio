from django.db import models
from django.utils import timezone

class Sensor(models.Model):
    serial_number = models.CharField(max_length=250, unique=True)
    name = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['id']

class Heartbeat(models.Model):
    serial_number = models.CharField(max_length=250)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['id']
