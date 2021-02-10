from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Man, Person, Woman

# Create your tests here.


class PersonAPITest(APITestCase):
    def setUp(self):
        # Populate database with some test data
        self.test_persons = [
            Woman.objects.create(
                name="Kmi Guzman", dni="96092912972", date_of_birth="1996-09-29"
            ),
            Woman.objects.create(
                name="Zhuyen Medina", dni="72012823441", date_of_birth="1972-01-28"
            ),
            Woman.objects.create(
                name="Lourdes Sanchez", dni="70042012979", date_of_birth="1970-04-20"
            ),
            Woman.objects.create(
                name="Dani Guzman", dni="98021512972", date_of_birth="1998-02-15"
            ),
            Woman.objects.create(
                name="Jane Doe", dni="56092912972", date_of_birth="1956-09-29"
            ),
            Man.objects.create(
                name="Adri Gonzalez", dni="96010911144", date_of_birth="1996-01-09"
            ),
            Man.objects.create(
                name="Tomas Gonzalez", dni="66040712988", date_of_birth="1966-04-07"
            ),
            Man.objects.create(
                name="Jhon Doe", dni="86092912972", date_of_birth="1986-09-29"
            ),
            Man.objects.create(
                name="Thoros Doe", dni="56092912977", date_of_birth="1956-09-29"
            ),
            Man.objects.create(
                name="Kurt Doe", dni="96092011832", date_of_birth="1996-09-20"
            ),
        ]

        # Store create url
        self.create_man_url = reverse("persons-create-man")
        self.create_woman_url = reverse("persons-create-woman")

    def test_person_create(self):
        data = {
            "name": "AName Anonymous",
            "dni": "01234567890",
            "date_of_birth": "1999-01-09",
        }

        r = self.client.post(self.create_man_url, data, format="json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED, repr(r.data))
        # Test that a person record was created
        self.assertEqual(Person.objects.all().count(), 11)
        # Test that a man was created
        self.assertEqual(Man.objects.all().count(), 6)
        self.assertEqual(Woman.objects.all().count(), 5)
        self.assertEqual(Man.objects.last().name, "AName Anonymous")

    def test_woman_create(self):
        data = {
            "name": "AName Anonymous",
            "dni": "01234567890",
            "date_of_birth": "1999-01-09",
        }

        r = self.client.post(self.create_woman_url, data, format="json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED, repr(r.data))
        self.assertEqual(Person.objects.all().count(), 11)
        self.assertEqual(Woman.objects.all().count(), 6)
        self.assertEqual(Woman.objects.last().dni, "01234567890")

    def test_person_update(self):
        pass

    def test_person_delete(self):
        pass

    def test_person_detail(self):
        pass

    def test_person_get_women(self):
        pass

    def test_person_get_men(self):
        pass

    def test_person_search_by_age(self):
        pass

    def test_person_search_by_name(self):
        pass

    def test_person_search_by_lastname(self):
        pass

    def test_person_search_by_disease(self):
        pass

    def test_person_search_by_observation(self):
        pass

    def test_person_mixed_query(self):
        pass