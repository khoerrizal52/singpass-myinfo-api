from django.urls import path
from .views import singpass_auth, singpass_auth_callback

urlpatterns = [
    path('', singpass_auth, name='singpass_auth'),
    path('callback', singpass_auth_callback, name='singpass_auth_callback'),
]
