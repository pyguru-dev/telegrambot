from django.urls import path
from authorization.views import *

urlpatterns = [
	path('authorization/', authorization),
]
