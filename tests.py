from django.test import TestCase
from datacenter.models import Schoolkid, Mark, Chastisement, Commendation
from schoolkid_script import (
    create_commendation, remove_chastisements, fix_marks, get_schoolkid
)

from django.test import Client


class CommendationTest(TestCase):
    fixtures = ['subject.json', 'teacher.json', 'test_chastisement.json',
                'test_schoolkid.json', 'test_lesson.json', 'test_mark.json']

    schoolkid_name = 'Фролов Иван'  # 'Голубев Феофан'

    schoolkid = get_schoolkid(schoolkid_name)

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_fix_mark(self):
        bad_marks = Mark.objects.filter(
            schoolkid=self.schoolkid, points__in=(2, 3)
        )
        self.assertTrue(bad_marks)
        response = self.client.get('/schoolkid/{}/'.format(self.schoolkid.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                               '<td style="text-align:center;">2 </td>')
        bad_marks = Mark.objects.filter(
            schoolkid=self.schoolkid, points__in=(2, 3)
        )
        fix_marks(self.schoolkid_name)
        self.assertFalse(bad_marks)
        # obj.refresh_from_db()
        response = self.client.get('/schoolkid/{}/'.format(self.schoolkid.id))
        self.assertNotContains(response,
                            '<td style="text-align:center;">2 </td>')
        self.assertNotContains(response,
                            '<td style="text-align:center;">3 </td>')

    def test_remove_chastisements(self):
        chastisements = Chastisement.objects.filter(schoolkid=self.schoolkid)
        self.assertTrue(chastisements)

        remove_chastisements(self.schoolkid_name)

        chastisements = Chastisement.objects.filter(schoolkid=self.schoolkid)
        self.assertFalse(chastisements)
        response = self.client.get('/schoolkid/{}/'.format(self.schoolkid.id))
        self.assertNotContains(response, 'Замечания от учителей')

    def test_create_commendation(self):
        commendation = Commendation.objects.filter(schoolkid=self.schoolkid)
        self.assertFalse(commendation)

        commendation = create_commendation(self.schoolkid_name, 'Математика')

        self.assertTrue(commendation)
        response = self.client.get('/schoolkid/{}/'.format(self.schoolkid.id))
        self.assertContains(response, commendation.text)


