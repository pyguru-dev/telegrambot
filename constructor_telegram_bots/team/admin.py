from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _

from .models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(TranslationAdmin):
	date_hierarchy = 'date_joined'
	list_filter = ('speciality',)

	list_display = ('username', 'speciality', 'date_joined')
	fields = ('image', 'username', 'speciality', 'date_joined')
