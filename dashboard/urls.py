from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.dashboard, name='dashboard'),
    path('clientes/', views.clientes, name='clientes'),
    path('chats/', views.chats, name='chats'),
    path('configuracion/', views.configuracion, name='configuracion'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),

    path('webhook/', views.webhook, name='webhook'),

    path('logout/', views.logout_view, name='logout'),

    path(
    'logs/',
    views.logs,
    name='logs'
),

path(
    'diccionario-datos/',
    views.diccionario_datos,
    name='diccionario_datos'
),
path(
    'descargar-vista/<str:nombre>/',
    views.descargar_vista,
    name='descargar_vista'
),


]