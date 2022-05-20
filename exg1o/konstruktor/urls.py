from django.urls import path
from konstruktor.views import *

urlpatterns = [
	path('konstruktor/<str:nickname>/', konstruktor),
	path('konstruktor/<str:nickname>/add_bot/', add_bot),
]
