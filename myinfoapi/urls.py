from django.urls import path
from .views import home, singpass_auth, singpass_auth_callback

urlpatterns = [
    path('', home, name='home'),
    path('singpass-auth', singpass_auth, name='singpass_auth'),
    path('singpass-auth/callback', singpass_auth_callback, name='singpass_auth_callback'),
]
