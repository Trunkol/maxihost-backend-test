"""zombies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from rest_framework.authtoken import views as auth_views
from rest_framework.routers import DefaultRouter

from survivor.views import SurvivorViewSet
from users.views import UserViewSet

router = DefaultRouter()
router.register(r'survivor', SurvivorViewSet, basename='survivors')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    url(r'^api-token-auth/', auth_views.obtain_auth_token),
    path('api/v1/', include(router.urls)),
]
