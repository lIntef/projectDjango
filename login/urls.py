from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('dashboardDoc/', views.dashboardDoc, name="dashboardDoc")
]