from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _

from .models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(TranslationAdmin):
	date_hierarchy = 'joined_date'
	list_filter = ('speciality',)

	list_display = ('id', 'username', 'speciality', 'joined_date')
	fields = ('image', 'username', 'speciality', 'joined_date')
