from django.urls import path
from . import views

urlpatterns = [
    path("create/man", views.CreateManApiView.as_view(), name="persons-create-man"),
    path(
        "create/woman", views.CreateWomanApiView.as_view(), name="persons-create-woman"
    ),
]