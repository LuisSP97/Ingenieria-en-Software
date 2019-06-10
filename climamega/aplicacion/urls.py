from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),  
    path('catalogo/', views.catalogo, name='catalogo'),
    path('catalogo/<int:codigo>/', views.producto, name='producto'),
    path('cotizacion/', views.cotizaciones, name='cotizaciones'),
    path('cotizacion/<int:numero_cotizacion>/', views.cotizacion, name='cotizacion'),
    path('cotizacion/nueva/', views.nuevaCotizacion, name='nuevaCotizacion'),
    path('cotizacion/generarCotizacion', views.generarCotizacion, name='generarCotizacion'),
]


