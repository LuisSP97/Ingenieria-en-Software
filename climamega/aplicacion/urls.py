from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),  
    path('catalogo/', views.catalogo, name='catalogo'),
    path('catalogo/<int:codigo>/', views.producto, name='producto'),
]


