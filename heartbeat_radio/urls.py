"""heartbeat_radio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework import routers
from studio import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

# Wire up our API using automatic URL routing for the user list.
urlpatterns = [
    path('', views.index, name='index'),
    path('api/admin/', include(router.urls)),
    path('api/', include('studio.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('django_plotly_dash/', include('django_plotly_dash.urls'))
]