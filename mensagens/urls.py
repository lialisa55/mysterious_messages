from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),  # Página inicial com a lista de salas
    path('room/<int:room_id>/', views.room, name='room'),  # Sala específica de chat
    path('room/<int:room_id>/send_message/', views.send_message, name='send_message'),  # Enviar mensagem na sala
    path('register/', views.register, name='register'),  # Página de registro
    path('login/', views.login_view, name='login'),  # Página de login
    path('profile/', views.profile, name='profile'),  # Adicione a view de perfil
    path('create_room/', views.create_room, name='create_room'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
