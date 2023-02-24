from django.urls import path
from personal_cabinet.views import *

urlpatterns = [
	path('', personal_cabinet),
]