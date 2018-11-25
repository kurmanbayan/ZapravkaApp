from django.urls import path
from authlog import views

urlpatterns = [
    path("login/", views.login),
    path("register/", views.register),
]
