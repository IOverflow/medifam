import re
from typing import Optional
from django_filters import CharFilter
from .models import Person
from django_filters.rest_framework import FilterSet
import django_filters as filters
from django.db.models.query_utils import Q
from django.db.models.query import QuerySet
from .filter_parser import logical_parser

def build_args(operator: str, left: int, right: Optional[int]):
    if operator == "+":
        return lambda x: x.age > left
    elif operator == "=":
        return lambda x: x.age == left
    elif operator == "-":
        return lambda x: x.age < left
    elif operator == ":" and right is not None:
        return lambda x: left <= x.age <= right
    return None


class PersonFilterSet(FilterSet):
    age = CharFilter(
        field_name="age",
        method="filter_age",
        label="Age filter expression",
    )
    name = filters.CharFilter(lookup_expr="icontains")
    address = filters.CharFilter(lookup_expr="icontains")
    observations = filters.CharFilter(method="parse_text")
    diseases = filters.CharFilter(method="parse_text")
    risk_factors = filters.CharFilter(lookup_expr="parse_text")
    year_of_birth = filters.DateFilter(field_name="date_of_birth", lookup_expr="year")
    not_name = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        exclude=True,
    )
    not_age = CharFilter(
        field_name="age",
        method="filter_age",
        label="Age filter expression",
        exclude=True,
    )
    not_doner = filters.BooleanFilter(field_name="doner", exclude=True)
    not_smokes = filters.BooleanFilter(field_name="smokes", exclude=True)
    not_alcoholic = filters.BooleanFilter(field_name="alcoholic", exclude=True)
    not_drinks_coffee = filters.BooleanFilter(field_name="drinks_coffee", exclude=True)
    not_year_of_birth = filters.DateFilter(
        field_name="date_of_birth",
        lookup_expr="year",
        exclude=True,
    )
    not_date_of_birth = filters.BooleanFilter(field_name="date_of_birth", exclude=True)

    class Meta:
        model = Person
        fields = (
            "dni",
            "doner",
            "alcoholic",
            "smokes",
            "drinks_coffee",
            "date_of_birth",
            "drinks_coffee",
            "history_id",
        )

    def filter_age(self, queryset, name, value):
        args = None
        age_regex = re.compile(
            r"(?P<operator>(\+)|(\-)|(\:)|(\=))\s*(?P<left>\d+)\s*([yY]\s*(?P<right>\d+))?",
            re.IGNORECASE,
        )
        if value:
            match = age_regex.search(value)
            if match:
                gd = match.groupdict()
                operator = gd["operator"]
                left = int(gd["left"])
                right = None
                if operator == ":" and gd.get("right", None):
                    right = int(gd["right"])
                args = build_args(operator, left, right)
        if args:
            q_ids = [x.pk for x in Person.objects.all() if args(x)]
            return queryset.filter(pk__in=q_ids)
        else:
            return Person.objects.none()

    def filter_text(self, queryset: QuerySet, name: str, value: str):
        # Split a multi request into values to join in an AND operation
        q= Q()
        values = value.split()

        for val in values:
            if val.startswith("-"):
                val = val[1:]
                q &= ~Q(**{f"{name}__icontains": val})
            else:
                q &= Q(**{f"{name}__icontains": val})

        return queryset.filter(q)

    def parse_text(self, queryset: QuerySet, name: str, value: str)-> QuerySet:
        # get the ast
        node = logical_parser.parse(value)
        # evaluate the ast
        q_expr = logical_parser.evaluate(node, name)
        return queryset.filter(q_expr)
