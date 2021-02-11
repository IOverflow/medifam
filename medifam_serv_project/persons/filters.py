import re
from typing import Any, Dict, Optional
from django.db.models.query import QuerySet
from rest_framework.request import Request
from .models import Person, Woman
from django_filters.rest_framework import FilterSet


def build_args(operator: str, left: int, right: Optional[int]) -> Dict[str, Any]:
    args = {}
    if operator == "+":
        args["age__gt"] = left
    elif operator == "=":
        args["age__exact"] = left
    elif operator == "-":
        args["age__lt"] = right
    elif operator == ":" and right is not None:
        args["age__range"] = [left, right]
    return args


def parse_request(request: Request):
    """
    Description:
    -----------
    Parses an Http GET request's querystring to know
    when to compare dates by lt, gt or range. This method
    only deals with:

    - age parameter
    -

    Parameter:
    ----------
    @request: rest_framework.Request

    Return:
    -------
    val: dict - Key/Value pairs of keys to filter by value.

    Example:
    --------
    parse_request("http://example.com/api/persons/woman/?age=+20")
    >>> val : {age__gt: 20}
    """
    age_regex = re.compile(
        r"age=(?P<operator>(\+)|(\-)|(\:)(\=))\s*(?P<left>\d+)\s*([yY]\s*(?P<right>\d+))?",
        re.IGNORECASE,
    )
    age_str = request.query_params.get("age", None)
    if age_str:
        match = age_regex.search(age_str)
        if match:
            gd = match.groupdict()
            operator = gd["operator"]
            left = int(gd["left"])
            right = None
            if operator == ":" and gd.get("right", None):
                right = int(gd["right"])
            return build_args(operator, left, right)
    return {}


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

    @property
    def qs(self):
        queryset = super().qs
        args = parse_request(self.request)
        if args:
            return queryset.filter(**args)
        else:
            return queryset