from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('dashboardDoc/', views.dashboardDoc, name="dashboardDoc"),
    path('loginregister/', views.registrarme, name="loginregister"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('signout/', views.signout, name="signout"),
    path('configuracion/', views.configuracion, name="configuracion"),
    path('editaraccount/', views.editaraccount, name="editaraccount"),
    path('correo/', views.correo, name="correo"),
    path('calendario/', views.calendario, name="calendario"),
    path('agendarcita/', views.agendarcita, name="agendarcita"),
    path('editarcita/', views.editarcita, name="editarcita"),
    path('newhistoriaclinica/', views.newhistoriaclinica, name="newhistoriaclinica"),
    path('historias/', views.historias, name="historias"),
    path('agregarfechas/', views.agregarfechas, name="agregarfechas"),
    path('base/', views.base, name="base"),
]