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

    path('detalleCliente/<int:rut>/', views.detalleCliente, name='detalleCliente'),

    path('clientes/nuevoCliente/', views.generarCliente, name='generarCliente'),

    path('buscarCliente/', views.buscarCliente, name='buscarCliente'),
    
    path('eliminarCliente/', views.eliminarCliente, name='eliminarCliente'),
    path('confirmarEliminarCliente/<int:rut>/', views.confirmarEliminarCliente, name='confirmarEliminarCliente'),

    path('modificarCliente/', views.modificarCliente, name='modificarCliente'),
    path('confirmarModificarCliente/<int:rut>', views.confirmarModificarCliente, name='confirmarModificarCliente'),

    path('detalleCotizacion/<int:codigo>/', views.detalleCotizacion, name='detalleCotizacion'),
    
    path('nuevaCotizacion/', views.nuevaCotizacion, name='nuevaCotizacion'),
    path('buscarCotizacion/', views.buscarCotizacion, name='buscarCotizacion'),
    path('crearCotizacion/', views.crearCotizacion, name='crearCotizacion'),


    path('detalleProducto/<int:codigo>/', views.detalleProducto, name='detalleProducto'),

    path('buscarCatalogo/', views.buscarCatalogo, name='buscarCatalogo'),
    path('agregarProducto/', views.agregarProducto, name='agregarProducto'),

    path('modificarProducto/', views.modificarProducto, name='modificarProducto'),
    path('confirmarModificarProducto/<int:codigo>/', views.confirmarModificarProducto, name='confirmarModificarProducto'),
    
    path('eliminarProducto/', views.eliminarProducto, name='eliminarProducto'),
    path('confirmarEliminarProducto/<int:codigo>/', views.confirmarEliminarProducto, name='confirmarEliminarProducto'),

    path('admin/', admin.site.urls),
]
