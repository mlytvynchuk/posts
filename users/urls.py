
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(template_name='usr/logout.html'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='usr/login.html'), name='login'),
]
