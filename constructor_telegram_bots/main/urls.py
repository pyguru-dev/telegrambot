from django.urls import path
from main.views import *

urlpatterns = [
	path('', main_page),
	path('view_site_user_profile/<int:other_user_id>/', view_site_user_profile_page)
]
