from django.urls import path
from survivor import views

urlpatterns = [
    path('', views.survivor_list),
    path('<int:pk>/', views.survivor_detail),
]