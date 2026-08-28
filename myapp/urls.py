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
    path('posts/', views.posts_list, name='posts'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),

    # API endpoints
    path('api/profile/<int:member_id>/', views.api_profile, name='api_profile'),
    path('api/posts/', views.api_posts, name='api_posts'),
    path('api/posts/<int:post_id>/', views.api_post_detail, name='api_post_detail'),
]
