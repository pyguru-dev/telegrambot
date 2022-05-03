from django.urls import path
from registration.views import *

urlpatterns = [
	path('registration/', registration),
	path('registration/register_account/', register_account),
]
