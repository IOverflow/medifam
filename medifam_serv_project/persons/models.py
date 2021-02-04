from django.db import models
from django.db.models.enums import TextChoices


class Person(models.Model):
    """
    Abstract person model to hold common person properties.
    This model should not be directly created, instead we
    must create Woman or Man objects.
    """

    # Every person has a name (obviously), here goes last name too
    name = models.CharField(max_length=250, blank=False, null=False)

    # Every person has a DNI (CI in CUBA)
    dni = models.CharField(max_length=11, blank=True, null=True, unique=True)

    # Store a person's address, if known
    address = models.CharField(max_length=250, blank=True, null=True)

    # Clinic resume number
    history_id = models.CharField(max_length=150, blank=True, null=True)

    # Date of birth
    date_of_birth = models.DateField(blank=False, null=False)

    # Store observations about this person
    observations = models.TextField(blank=True, null=True)

    # We might want to know if is a doner
    doner = models.BooleanField(default=False, blank=True, null=True)

    # We might want to know if is an alcoholic
    alcoholic = models.BooleanField(default=False, blank=True, null=True)

    # Does he drink coffee?? (If he's a programmer, then True by default)
    drinks_coffee = models.BooleanField(default=False, blank=True, null=True)

    # Does he smoke?
    smokes = models.BooleanField(default=False, blank=True, null=True)

    # Diseases that this person suffers
    diseases = models.TextField(null=True, blank=True)

    # Risk factors
    risk_factors = models.TextField(null=True, blank=True)


class EndPregnancyCauseChoices(TextChoices):
    ABORTION = "Abortion", "Abortion"
    NATURAL_BIRTH = "NATURAL_BIRTH", "Natural birth"
    CAESAREAN = "Caesarean", "Caesarean operation"


class Woman(Person):
    """
    Represents a woman. It has all the properties from
    person and also stores cytological tests, pregnances, etc.
    """

    pass


class Man(Person):
    pass


class CytologicalTest(models.Model):
    date = models.DateField(blank=False, null=False)
    observations = models.TextField(blank=True, null=True)
    woman = models.ForeignKey(Woman, on_delete=models.CASCADE, blank=False, null=False)


class Pregnance(models.Model):
    date_start = models.DateField(blank=False, null=False)
    date_end = models.DateField(blank=True, null=True)
    end_cause = models.CharField(
        choices=EndPregnancyCauseChoices.choices,
        blank=True,
        null=True,
    )
    active = models.BooleanField(default=False)
    woman = models.ForeignKey(Woman, on_delete=models.CASCADE, blank=False, null=False)


class HomeLockdown(models.Model):
    date_start = models.DateField(blank=False, null=False)
    date_end = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)