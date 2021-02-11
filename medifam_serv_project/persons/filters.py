from django.db.models.query import QuerySet
from rest_framework.request import Request
from medifam_serv_project.persons.models import Person, Woman
from django_filters.rest_framework import FilterSet


def parse_request(request: Request):
    pass


class PersonFilterSet(FilterSet):
    class Meta:
        model = Person
        fields = {
            "name": ["icontains"],
            "dni": ["iexact"],
            "address": ["icontains"],
            "history_id": ["iexact"],
            "date_of_birth": ["exact", "year__exact"],
            "observations": ["icontains"],
            "doner": ["exact"],
            "alcoholic": ["exact"],
            "drinks_coffee": ["exact"],
            "smokes": ["exact"],
            "diseases": ["icontains"],
            "risk_factors": ["icontains"],
        }

    def filter_by_years(self, queryset: QuerySet, name: str, value):
        request = self.request
        # Parse the request to know if filter for lt, gt or in
        args = parse_request(request)
        if args:
            return queryset.filter(**args)
        else:
            return queryset