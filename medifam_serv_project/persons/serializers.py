from .models import (
    CytologicalTest,
    HomeLockdown,
    Man,
    Pregnance,
    Woman,
)
from rest_framework.serializers import ModelSerializer


class HomeLockdownSerializer(ModelSerializer):
    class Meta:
        model = HomeLockdown
        fields = [
            "date_start",
            "date_end",
            "active",
        ]


class ManSerializer(ModelSerializer):
    home_lockdowns = HomeLockdownSerializer(many=True, required=False)

    class Meta:
        model = Man
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
        ]


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
