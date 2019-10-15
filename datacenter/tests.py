from django.test import TestCase
from .models import Schoolkid, fix_marks, create_commendation, remove_chastisements
from datetime import datetime
from django.test import Client




class CommendationTest(TestCase):
    fixtures = ['subject.json', 'teacher.json',
                'test_schoolkid.json', 'test_lesson.json', 'test_mark.json']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()


    def test_mark(self):
        schoolkid = Schoolkid.objects.filter(
            full_name__contains='Фролов Иван'
        ).get()
        schoolkid2 = Schoolkid.objects.filter(
            full_name__contains='Голубев Феофан'
        ).get()

        # self.assertEqual(response.status_code, 200)
        fix_marks(schoolkid)
        # obj.refresh_from_db()
        response = self.client.get('/schoolkid/6551/')
        self.assertContains(response,
                            '<td style="text-align:center;">2 </td>')
        self.assertContains(response,
                            '<td style="text-align:center;">3 </td>')






    # commendation = create_commendation('Фролов Иван', 'Математика')


    # def setUp(self):

