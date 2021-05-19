from django.contrib import admin
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("home", views.homepage, name="homepage"),
    path('admin/', admin.site.urls),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
]
