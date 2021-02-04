from rest_framework.test import APITestCase
from .models import Man, Woman

# Create your tests here.

class PersonAPITest(APITestCase):
    def setup(self):
        # Populate database with som test data
        self.test_persons = [

        ]

    def test_person_create(self):
        pass

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