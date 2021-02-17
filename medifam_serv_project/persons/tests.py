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
                name="Kmi Guzman",
                dni="96092912972",
                date_of_birth="1996-09-29",
                diseases="Diabetes, EPOC",
            ),
            Woman.objects.create(
                name="Zhuyen Medina",
                dni="72012823441",
                date_of_birth="1972-01-28",
                diseases="HA, Stress",
            ),
            Woman.objects.create(
                name="Lourdes Sanchez",
                dni="70042012979",
                date_of_birth="1970-04-20",
            ),
            Woman.objects.create(
                name="Dani Guzman",
                dni="98021512972",
                date_of_birth="1998-02-15",
                diseases="Diabetes",
            ),
            Woman.objects.create(
                name="Jane Doe",
                dni="56092912972",
                date_of_birth="1956-09-29",
                diseases="Diabetes, HA",
            ),
            Man.objects.create(
                name="Adri Gonzalez",
                dni="96010911144",
                date_of_birth="1996-01-09",
            ),
            Man.objects.create(
                name="Tomas Gonzalez",
                dni="66040712988",
                date_of_birth="1966-04-07",
            ),
            Man.objects.create(
                name="Jhon Doe",
                dni="86092912972",
                date_of_birth="1986-09-29",
            ),
            Man.objects.create(
                name="Thoros Doe",
                dni="56092912977",
                date_of_birth="1956-09-29",
                diseases="Diabetes",
            ),
            Man.objects.create(
                name="Kurt Doe",
                dni="96092011832",
                date_of_birth="1996-09-20",
            ),
        ]

        # Store create url
        self.create_man_url = reverse("persons-create-man")
        self.create_woman_url = reverse("persons-create-woman")

        # Filter woman url
        self.filter_woman = reverse("retrieve-woman", kwargs={"dni": "96092912972"})
        # Filter man url
        self.filter_man = reverse("retrieve-man", kwargs={"dni": "96010911144"})

    def test_man_create(self):
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
        dni = "96010911144"
        url = reverse("retrieve-person", kwargs={"dni": dni})
        response = self.client.get(url)

        fields = [
            "dni",
            "age",
            "address",
            "risk_factors",
            "observations",
            "diseases",
            "date_of_birth",
            "smokes",
            "alcoholic",
            "doner",
            "history_id",
        ]

        self.assertEqual(response.data["name"], "Adri Gonzalez")
        self.assertTrue(all(x in response.data for x in fields))

    def test_person_get_women(self):
        response = self.client.get(self.filter_woman)
        # Assert we found it
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data
        self.assertTrue("name" in response_data)
        self.assertTrue("dni" in response_data)
        self.assertTrue("age" in response_data)
        self.assertEqual("96092912972", response_data["dni"])
        # Account for current age, not just year substraction
        self.assertEqual(response_data["age"], 24)

    def test_person_get_men(self):
        response = self.client.get(self.filter_man)
        # Assert we found it
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data
        self.assertTrue("name" in response_data)
        self.assertTrue("dni" in response_data)
        self.assertTrue("age" in response_data)
        self.assertEqual("96010911144", response_data["dni"])
        # Account for current age, not just year substraction
        self.assertEqual(response_data["age"], 25)

    def test_get_all(self):
        url = reverse("person-filter", kwargs={"gender": "all"})
        woman_url = reverse("person-filter", kwargs={"gender": "woman"})
        man_url = reverse("person-filter", kwargs={"gender": "man"})
        response = self.client.get(url)
        # Assert we got an OK response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert we got all persons in db
        self.assertEqual(Person.objects.all().count(), len(response.data))

        response = self.client.get(woman_url)
        # assert we got an ok response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert we got all women
        self.assertEqual(Woman.objects.all().count(), len(response.data))

        response = self.client.get(man_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Man.objects.all().count(), len(response.data))

    def test_person_search_by_age(self):
        query = {"age": "=25"}
        url = reverse("person-filter", kwargs={"gender": "all"})
        response = self.client.get(url, data=query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert we found only one with exact 25 years old (untill 2022)
        self.assertEqual(len(response.data), 1)
        # Assert it is Adri
        self.assertEqual(response.data[0]["name"], "Adri Gonzalez")

        # Test less than
        query["age"] = "-25"
        response = self.client.get(url, data=query)
        self.assertEqual(len(response.data), 3)
        self.assertTrue("Dani Guzman" in [x["name"] for x in response.data])

        # Test range
        query["age"] = ":25 y 60"
        response = self.client.get(url, data=query)
        self.assertEqual(len(response.data), 5)
        self.assertTrue("Tomas Gonzalez" in [x["name"] for x in response.data])

    def test_person_search_by_name(self):
        query = {
            "name": "Kmi Guzman",
        }
        url = reverse("person-filter", kwargs={"gender": "all"})
        response = self.client.get(url, data=query)
        # Assert there's only one
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Assert it has dni = 96092912972
        self.assertEqual(response.data[0]["dni"], "96092912972")

    def test_person_search_by_lastname(self):
        # Arrange
        query = {"name": "Gonzalez"}
        url = reverse("person-filter", kwargs={"gender": "all"})

        # Act
        response = self.client.get(url, data=query)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        names = [x["name"] for x in response.data]
        self.assertTrue("Adri Gonzalez" in names)
        self.assertTrue("Tomas Gonzalez" in names)

    def test_person_search_by_disease(self):
        pass

    def test_person_search_by_observation(self):
        pass

    def test_person_mixed_query(self):
        # Test #1: Search persons under 25 age with diabetes
        query = {"age": "-25", "diseases": "diabetes"}
        url = reverse("person-filter", kwargs={"gender": "all"})
        response = self.client.get(url, data=query)

        # Test that we get only 2 results
        self.assertEqual(len(response.data), 2)
        names = [x["name"] for x in response.data]
        self.assertTrue("Kmi Guzman" in names)
        self.assertTrue("Dani Guzman" in names)

        # Test #2: Search persons under 60 and above 25 that
        # doesn't suffer of diabetes and suffers from HA
        query = {
            "age": ":25 y 50",
            "not_diseases": "Diabetes",
            "diseases": "HA",
        }

        # Test that we only get 1 result
        response = self.client.get(url, data=query)
        self.assertEqual(len(response.data), 1)
        self.assertTrue(response.data[0]["name"] == "Zhuyen Medina")