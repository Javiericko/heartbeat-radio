from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.shortcuts import render

from studio.serializers import SensorSerializer, HeartbeatSerializer, UserSerializer
from studio.models import Sensor, Heartbeat


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# Function based view for the dash app to monitor heartbeats
def index(request, *args, **kwargs):
    '''
    Return a dashboard of the amount of heartbeats per sensor
    '''

    return render(request, 'studio/base.html', context={})


class SensorListApiView(APIView):
    # Add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List
    def get(self, request, *args, **kwargs):
        '''
        List all the sensors that have been created
        '''
        sensors = Sensor.objects.all()
        serializer = SensorSerializer(sensors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create a sensor
        '''
        data = {
            "serial_number": request.data.get('serial_number'),
            "name": request.data.get('name'),
            "location": request.data.get('location')
        }

        serializer = SensorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SensorDetailApiView(APIView):
    # Add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, serial_number):
        '''
        Helper method to get the object with given serial_number
        '''
        try:
            return Sensor.objects.get(serial_number=serial_number)
        except Sensor.DoesNotExist:
            return None

    # 3. View
    def get(self, request, serial_number, *args, **kwargs):
        '''
        Retrieves the Sensor with given serial_number
        '''
        sensor_instance = self.get_object(serial_number)
        if not sensor_instance:
            return Response(
                {"response": "Object with serial number does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SensorSerializer(sensor_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, serial_number, *args, **kwargs):
        '''
        Updates the Sensor with given serial_number if it exists
        '''
        sensor_instance = self.get_object(serial_number)
        if not sensor_instance:
            return Response(
                {"response": "Object with serial number does not exist"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            "serial_number": request.data.get('serial_number'),
            "name": request.data.get('name'),
            "location": request.data.get('location')
        }
        serializer = SensorSerializer(instance=sensor_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, serial_number, *args, **kwargs):
        '''
        Deletes the Sensor with given serial_number if it exists
        '''
        sensor_instance = self.get_object(serial_number)
        if not sensor_instance:
            return Response(
                {"response": "Object with serial_number does not exist"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        sensor_instance.delete()
        return Response(
            {"response": "Sensor deleted!"},
            status=status.HTTP_200_OK
        )


class HeartbeatListApiView(APIView):
    # Add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List
    def get(self, request, *args, **kwargs):
        '''
        List all the heartbeats that have been created
        '''
        heartbeats = Heartbeat.objects.all()
        serializer = HeartbeatSerializer(heartbeats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create a heartbeat
        '''
        data = {
            "serial_number": request.data.get('serial_number'),
        }

        serializer = HeartbeatSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HeartbeatDetailApiView(APIView):
    # Add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, heartbeat_id):
        '''
        Helper method to get the object with given heartbeat_id
        '''
        try:
            return Heartbeat.objects.get(id=heartbeat_id)
        except Heartbeat.DoesNotExist:
            return None

    # 3. View
    def get(self, request, heartbeat_id, *args, **kwargs):
        '''
        Retrieves the Heartbeat with given heartbeat_id
        '''
        heartbeat_instance = self.get_object(heartbeat_id)
        if not heartbeat_instance:
            return Response(
                {"response": "Object with heartbeat id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = HeartbeatSerializer(heartbeat_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)