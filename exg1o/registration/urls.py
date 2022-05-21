from django.urls import path
from registration.views import *

urlpatterns = [
	path('registration/', registration_page),
	path('registration/register_account/', register_account),
]
