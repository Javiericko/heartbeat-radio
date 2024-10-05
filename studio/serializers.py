from django.contrib.auth.models import User
from rest_framework import serializers
from studio.models import Sensor, Heartbeat


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'serial_number', 'name', 'location', 'date_created']


class HeartbeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heartbeat
        fields = ['id', 'serial_number', 'date_created']