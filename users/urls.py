from django.urls import path
from .views import (
    CustomRegisterView,
    CustomLoginView,
    CustomLogoutView,
    ProfileView,
)

urlpatterns = [
    path("register/", CustomRegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
]