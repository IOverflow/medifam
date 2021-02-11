from django.urls import path, re_path
from . import views

urlpatterns = [
    path("create/man", views.CreateManApiView.as_view(), name="persons-create-man"),
    path(
        "create/woman", views.CreateWomanApiView.as_view(), name="persons-create-woman"
    ),
    re_path(
        r"(?P<gender>(man)|(woman))",
        views.FilterPersonApiView.as_view(),
        name="person-filter",
    ),
]