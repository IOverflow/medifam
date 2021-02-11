from .models import (
    CytologicalTest,
    HomeLockdown,
    Man,
    Person,
    Pregnance,
    Woman,
)
from rest_framework.serializers import ModelSerializer, IntegerField


class HomeLockdownSerializer(ModelSerializer):
    class Meta:
        model = HomeLockdown
        fields = [
            "date_start",
            "date_end",
            "active",
        ]


class PersonSerializer(ModelSerializer):
    home_lockdowns = HomeLockdownSerializer(many=True, required=False)
    age = IntegerField(source="age")

    class Meta:
        model = Person
        fields = [
            "name",
            "dni",
            "address",
            "history_id",
            "date_of_birth",
            "age",
            "observations",
            "doner",
            "alcoholic",
            "drinks_coffee",
            "smokes",
            "diseases",
            "risk_factors",
            "home_lockdowns",
        ]
        read_only_fields = ("age",)


class ManSerializer(PersonSerializer):
    class Meta:
        model = Man


class PregnancySerializer(ModelSerializer):
    class Meta:
        model = Pregnance
        fields = [
            "date_start",
            "date_end",
            "end_cause",
        ]


class CytologicalTestSerializer(ModelSerializer):
    class Meta:
        model = CytologicalTest
        fields = [
            "date",
            "observations",
        ]


class WomanSerializer(ModelSerializer):
    home_lockdowns = HomeLockdownSerializer(many=True, required=False)
    pregnancies = PregnancySerializer(many=True, required=False)
    cytological_tests = CytologicalTestSerializer(many=True, required=False)

    class Meta:
        model = Woman
        fields = [
            "name",
            "dni",
            "address",
            "history_id",
            "date_of_birth",
            "observations",
            "doner",
            "alcoholic",
            "drinks_coffee",
            "smokes",
            "diseases",
            "risk_factors",
            "home_lockdowns",
            "pregnancies",
            "cytological_tests",
        ]
