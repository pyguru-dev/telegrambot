from django.contrib import admin

from django.utils.translation import gettext_lazy as _

from team.models import TeamMembers


@admin.register(TeamMembers)
class TeamMembersAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_filter = ('speciality_en', 'speciality_uk', 'speciality_ru')

	list_display = (
		'username',
		'speciality_en',
		'speciality_uk',
		'speciality_ru',
		'date_joined'
	)

	fields = (
		'image',
		'username',
		'speciality_en',
		'speciality_uk',
		'speciality_ru',
		'date_joined'
	)
