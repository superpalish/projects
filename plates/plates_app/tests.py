import json

from django.test import TestCase

# Create your tests here.
from django.core.exceptions import ValidationError

from plates_app.models import NumberPlate
from plates_app.serializers import make_dict, add_dict_to_list


class NumberPlateViewSet(TestCase):
    create_data = """
        {
            "plates_number": "в505тс78rus",
            "car_model": "Altima",
            "owners": [
                {
                    "first_name": "Elena",
                    "last_name": "Ivkina",
                    "middle_name": "K",
                    "document": {
                        "id_type": "DL",
                        "value": "PV11171"
                    }
                },
                {
                    "first_name": "Alena",
                    "last_name": "Ivkina",
                    "middle_name": "K",
                    "document": {
                        "id_type": "PT",
                        "value": "100071"
                    }
                }
            ]
        }
    """

    update_data = """
        {
            "id": 1,
            "plates_number": "в555тс198rus",
            "car_model": "Logan2",
            "owners": [
                {
                    "id": %d,
                    "first_name": "Helena",
                    "last_name": "Ivkina",
                    "middle_name": "N",
                    "document": {
                        "id": 1,
                        "id_type": "DL",
                        "value": "PV0004"
                    }
                },
                {
                    "id": %d,
                    "first_name": "Olena",
                    "last_name": "Ivkina",
                    "middle_name": "K",
                    "document": {
                        "id": 2,
                        "id_type": "PT",
                        "value": "96500004"
                    }
                }
            ]
        }
    """

    def setUp(self):
        self.client.post('/api/v1/plates/', self.create_data, content_type="application/json")

    def test_create_works_correctly(self):
        response = self.client.get('/api/v1/plates/')
        resp = response.status_code
        self.assertTrue(resp == 200)
        created = NumberPlate.objects.all()[0]
        self.assertEqual(created.plates_number, "в505тс78rus")
        elena = created.owners.get(document__value="PV11171", document__id_type="DL")
        self.assertEqual(elena.first_name, "Elena")
        alena = created.owners.get(document__value="100071", document__id_type="PT")
        self.assertEqual(alena.first_name, "Alena")

    def test_update_works_correctly(self):
        target = NumberPlate.objects.all()[0]
        elena = target.owners.get(document__value="PV11171", document__id_type="DL")
        alena = target.owners.get(document__value="100071", document__id_type="PT")
        response = self.client.patch('/api/v1/plates/{}/'.format(target.id),
                                     self.update_data % (elena.id, alena.id),
                                     content_type="application/json")
        updated = NumberPlate.objects.all()[0]
        self.assertEqual(updated.plates_number, "в555тс198rus")
        owner = updated.owners.get(document__value="PV0004", document__id_type="DL")
        self.assertEqual(owner.first_name, "Helena")
        owner2 = updated.owners.get(document__value="96500004", document__id_type="PT")
        self.assertEqual(owner2.first_name, "Olena")

    def test_make_dict(self):
        d = {
            'country': 'Russia',
            'city': 'Moscow',
            'address': [
                {'street': 'Tverskaya'},
                {'house': 1}
            ],
            'person': {
                'name': 'Dmitry',
                'age': 40
            }
        }
        result = make_dict(
            d,
            include=['person'],
            exclude=['country', 'city', 'address'],
            add_dict={
                'country': 'USA',
                'city': 'Miami',
                'address': [
                    {'avenue': 'Best Resort'},
                    {'house': 1}
                ]
            }
        )
        expected = {
            'city': 'Miami',
            'country': 'USA',
            'person': {
                'age': 40,
                'name': 'Dmitry'
            },
            'address': [
                    {'avenue': 'Best Resort'},
                    {'house': 1}
            ]
        }
        self.assertEqual(result, expected)

    def test_add_dict_to_list(self):
        d = {
            'person': {
                'name': 'Dmitry',
                'age': 40
            }
        }
        result = add_dict_to_list(d)
        expected = [
            {
                'person': {
                    'name': 'Dmitry',
                    'age': 40
                }
            }
        ]
        self.assertEqual(result, expected)

    def test_regex_validator(self):
        plate = NumberPlate(plates_number="м11ло77rus", car_model='Buick')
        self.assertRaises(ValidationError, plate.full_clean)
