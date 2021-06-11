from django.contrib import admin
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("home", views.homepage, name="homepage"),
    path("calculator", views.calculator, name="calculator"),
    path("history", views.history, name="history"),
    path('admin/', admin.site.urls),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path('upload_waste/', views.upload_waste, name = 'upload-waste'),
    path('edit_waste/', views.edit_waste, name = 'edit-waste'),
]
