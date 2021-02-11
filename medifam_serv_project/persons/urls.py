from django.urls import path, re_path
from . import views

urlpatterns = [
    path("create/man", views.CreateManApiView.as_view(), name="persons-create-man"),
    path(
        "create/woman", views.CreateWomanApiView.as_view(), name="persons-create-woman"
    ),
    re_path(
        r"(?P<gender>(man)|(woman)|(all))/list",
        views.FilterPersonApiView.as_view(),
        name="person-filter",
    ),
    path(
        "woman/<str:dni>",
        views.RetrieveWomanApiView.as_view(),
        name="retrieve-woman",
    ),
    path(
        "man/<str:dni>",
        views.RetrieveManApiView.as_view(),
        name="retrieve-man",
    ),
    path(
        "all/<str:dni>",
        views.RetrievePersonApiView.as_view(),
        name="retrieve-person",
    ),
]