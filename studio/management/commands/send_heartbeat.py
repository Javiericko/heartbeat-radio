from django.core.management.base import BaseCommand
from urllib.request import urlopen
import json
import requests
from requests.auth import HTTPBasicAuth
import random

from studio.serializers import SensorSerializer
from studio.models import Sensor

class Command(BaseCommand):
    help = "Sends a heartbeat from a randomly selected sensor"

    def handle(self, *args, **options):
        
        # Get all of our sensors
        sensor = Sensor.objects.all()
        serializer = SensorSerializer(sensor, many=True)
        
        if serializer.is_valid:
            # Get a random sensor from our list
            random_sensor = random.choice(serializer.data)['serial_number']
        
        # Make a POST request to our heartbeat endpoint to create one

        payload = {"serial_number": random_sensor}
        
        # We could handle these passwords with a secrets manager or similar solution!
        response = requests.post("http://0.0.0.0:8000/api/heartbeat/", json=payload, auth=HTTPBasicAuth("admin", "admin"))

        if response.status_code == 201:
            print(f"send_heartbeat: {response.status_code} - {response.text}")

        else: # We could handle the error here
            print(f"send_heartbeat: {response.status_code} - {response.text}")