from django.urls import path
from . import views

urlpatterns = [
    path('', views.about, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('browse/', views.browse, name='browse'),
    path('messages/', views.view_messages, name='messages'),
    path('call/', views.call, name='call'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
