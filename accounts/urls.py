from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # URL for user registration page
    path('register/', views.register, name='register'),

    # URL for login page (using Django's built-in LoginView)
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'  # our custom login template
    ), name='login'),

    # URL for logout (handled by our custom logout function)
    path('logout/', views.logout_view, name='logout'),
]



