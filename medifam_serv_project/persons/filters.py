import re
from typing import Optional
from django_filters import CharFilter
from .models import Person
from django_filters.rest_framework import FilterSet


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
