from django.test import TestCase
from django.contrib.auth.models import User

from units.models import (
    Unit,
    # UnitUserProfile,
    # UnitSchedule
)

from ..tests.function_for_testing import (
    create_user,
    create_profile,
    create_unit,
    create_reservation,
    )


class APITestCase(TestCase):

    def setUp(self):
        user = create_user(username='alex')
        profile = create_profile(user=user)
        self.unit = create_unit(
            unit_name='Установка 1',
            unit_manager=profile,
            )

        print('self.unit', self.unit)

    def test(self):
        print('self', self)


        





# import datetime


# from django.test import Client



# class SimpleTest(unittest.TestCase):

#     def setUp(self):
#         # u = Unit.create()

#         self.client = Client()
#         self.client.login(username='alex', password='1q1q1q1q')

#     def test_details(self):
        
#         data_create = {
#             'unit': 1,
#             'start_work': datetime.datetime.now(),
#             'end_work': datetime.datetime.now(),
#             'tester': 1,
#             'test_object': 'Объект испытания1',
#             'distance': 1,
#             'note_text': 'Примечение 1',
#             }

#         # response = self.client.get('/api/units/')
#         response = self.client.post('/api/units/', data=data_create)
#         print('response', response)

#         self.assertEqual(response.status_code, 200)


# # def ATestCase(TestCase):
# #     c = Client()
# #     c.login(username='alex', password='1q1q1q1q')

# #     assert True
