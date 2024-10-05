from django.urls import path
from studio import views
from .views import (
    SensorListApiView,
    SensorDetailApiView,
    HeartbeatDetailApiView,
    HeartbeatListApiView,
)
from . import heartbeat_viewer

urlpatterns = [
    path('sensor/', SensorListApiView.as_view()),
    path('sensor/<int:serial_number>/', SensorDetailApiView.as_view()),
    path('heartbeat/', HeartbeatListApiView.as_view()),
    path('heartbeat/<int:heartbeat_id>/', HeartbeatDetailApiView.as_view()),
]