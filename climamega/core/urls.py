"""climamega URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from core import views
from django.conf import settings

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),  
    path('catalogo/', views.catalogo, name='catalogo'),
    path('catalogo/<int:codigo>/', views.producto, name='producto'),
    path('catalogo/nuevo/', views.nuevoProducto, name='nuevoProducto'),
    path('catalogo/nuevoProducto/', views.generarProducto, name='generarProducto'),
    path('cotizacion/', views.cotizaciones, name='cotizaciones'),
    path('cotizacion/<int:numero_cotizacion>/', views.cotizacion, name='cotizacion'),
    path('cotizacion/nueva/', views.nuevaCotizacion, name='nuevaCotizacion'),
    path('cotizacion/generarCotizacion/', views.generarCotizacion, name='generarCotizacion'),
    path('admin/', admin.site.urls),
]
