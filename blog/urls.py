from django.urls import path
from . import views
urlpatterns = [
    path('', views.lista_public, name='lista_public'),
    path('publicaciones/nueva', views.nueva_public, name='nueva_public'),
    path('publicaciones/<int:pk>/editar/', views.editar_public, name='editar_public'),
    path('evaluacion2/', views.evaluacion2, name='lista_equipos'),
    path('publicacion/<int:pk>/', views.detalle_public, name='detalle_public'),
]