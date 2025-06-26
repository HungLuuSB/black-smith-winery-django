from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="account/login"),
    path("signup", views.signup, name="account/signup"),
    path("logout", views.logout, name="account/logout"),
    path("edit", views.edit, name="account/edit"),
    path("dashboard", views.dashboard, name="account/dashboard"),
]
