from . import views
from django.urls import path

urlpatterns = [
    # Create URI is api/users/create/ --> account-create
    path("create/", views.UserCreateAPIView.as_view(), name="account-create"),
    path("login/", views.obtain_auth_token, name="account-login"),
]
