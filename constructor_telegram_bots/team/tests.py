from django.test import TestCase
from django.http import HttpResponse
from django import urls

from .models import TeamMember

from datetime import datetime


class TeamMemberModelTests(TestCase):
	def setUp(self) -> None:
		self.current_date: datetime = datetime.now()
		self.team_member: TeamMember = TeamMember.objects.create(
			username='test',
			speciality='Test',
			joined_date=self.current_date
		)

	def test_fields(self) -> None:
		self.assertEqual(str(self.team_member.image), '')
		self.assertEqual(self.team_member.username, 'test')
		self.assertEqual(self.team_member.speciality, 'Test')
		self.assertEqual(self.team_member.joined_date, self.current_date)

class ViewsTests(TestCase):
	def test_team_view(self) -> None:
		url: str = urls.reverse('team')
		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'team.html')
