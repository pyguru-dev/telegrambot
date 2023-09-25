from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(TranslationAdmin):
	date_hierarchy = 'joined_date'
	list_filter = ('speciality', 'joined_date')

	list_display = ('username_', 'speciality', 'joined_date')
	fields = ('image', 'username', 'speciality', 'joined_date')

	@admin.display(description='@username', ordering='username')
	def username_(self, team_member: TeamMember) -> str:
		return f'@{team_member.username}'
